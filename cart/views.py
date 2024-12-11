from django.shortcuts import render,HttpResponseRedirect
from .models import Cart,CartItem,order,OrderItem
from products.models import Product
from .forms import OrderForm
import uuid
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from superpet.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required


# Create your views here.
# we do redirect
@login_required(login_url="/login")
def add_to_cart(request, productId):
    print("**************",productId,"****************")
    print(request.user)
    currentUser=request.user
#   obj ,boolean=name           . method   (making current user object)
    cart,created=Cart.objects.get_or_create(user=currentUser)
    request.session["cart_id"]=cart.id
    #   ------------------     (cart of currentuser)    --------- 
 #                                                 (models=views,app_name=var_name.objects.method())
    cartitem,created=CartItem.objects.get_or_create(cart=cart,products=Product.customManager.get(id=productId))
#   variable=typecaste(         ("form input field name"))
    quantity=int(request.GET.get("quantity"))
    if created:
         cartitem.quantity=quantity      #obj.models
    else:
        cartitem.quantity=cartitem.quantity+quantity
#   for save data in workbench
    cartitem.save()
    return HttpResponseRedirect("/products")

# render
@login_required(login_url="/login")
def display_cart(request):
    currentUser=request.user
    cart=Cart.objects.get(user=currentUser)
    
  # var_name = obj.modes_name_set.all()
    cartitems=cart.cartitem_set.all()
    total=0
    for cartitem in cartitems:
        total+=cartitem.quantity*cartitem.products.product_price
    return render(request,"cart.html",{"cartitems":cartitems,"total":total})

login_required(login_url="/login")
def update_cart(request,cartItemId):
    cartitem=CartItem.objects.get(id=cartItemId)
    cartitem.quantity=request.GET.get("quantity")
    cartitem.save()
    return HttpResponseRedirect("/cart")

login_required(login_url="/login")
def delete_cartitem(request,cartItemId):
    cartitem=CartItem.objects.get(id=cartItemId)
    cartitem.delete()
    return HttpResponseRedirect("/cart")

login_required(login_url="/login")
def checkout(request):
    if request.method=="GET":
        form=OrderForm()
        print(request.session.get("cart_id"))
        return render(request, "checkout.html",{"form":form})
    # fetch data from form
    if request.method=="POST":
        form=OrderForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            Order=order.objects.create(order_id=uuid.uuid4().hex,
                                 user=request.user,
                                 address_line_1=form.cleaned_data["address_line_1"],
                                 address_line_2=form.cleaned_data["address_line_2"],
                                 city=form.cleaned_data["city"],
                                 state=form.cleaned_data["state"],
                                 pincode=form.cleaned_data["pincode"],
                                 phone_no=form.cleaned_data["phone_no"])
            cart_id=request.session["cart_id"]
            cart=Cart.objects.get(id=cart_id)
            cartitems=cart.cartitem_set.all()

#          jitne cartitem uthne orderitem 
            for cartitem in cartitems:
                OrderItem.objects.create(order=Order,quantity=cartitem.quantity,products=cartitem.products)
 #                                       (models=order_obj,models-order_var = itterator.cart_var)

    return HttpResponseRedirect("/cart/payment/"+Order.order_id)

def payment(request,orderId):
    Order=order.objects.get(order_id=orderId)
    orderitems=Order.orderitem_set.all()
    total=0
    for orderitem in orderitems:
        total+=orderitem.quantity*orderitem.products.product_price
    client=razorpay.Client(auth=("rzp_test_9OqmIDeq85cvr3","LVkt6Cs9VskcAarHG1ryJNdr"))
    data = { "amount": total*100, "currency": "INR", "receipt": orderId }
    payment = client.order.create(data=data)
    return render(request,"payment.html",{"payment":payment})

@csrf_exempt
def paymentSuccess(request,orderId):
    razorpay_response={
        "razorpay_payment_id":request.POST.get("razorpay_payment_id"),
        "razorpay_order_id":request.POST.get("razorpay_order_id"),
        "razorpay_signature":request.POST.get("razorpay_signature")

    }
    client=razorpay.Client(auth=("rzp_test_9OqmIDeq85cvr3","LVkt6Cs9VskcAarHG1ryJNdr"))
    payment_check=client.utility.verify_payment_signature(razorpay_response)
    if payment_check:
        print("order is paid")
        Order=order.objects.get(order_id=orderId)
        Order.paid=True
        Order.save()
        send_mail(f"[{order.order_id} placed]",
                  "Order Placed Successfully..",
                  EMAIL_HOST_USER,
                  ["soulehashaikh39@gmail.com"],
                  fail_silently=False)

    return render(request, "success.html")
