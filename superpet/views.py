from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from products.models import Product

def home(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def user_login(request):
    if request.method=="GET":
        return render(request,"login.html")
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            print(request.user.first_name)
            return HttpResponseRedirect("/products")
        else:
            return render(request,"login.html",{"message":"Login failed"})
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")




def register(request):
    if request.method=="GET":
        #form=UserCreationForm()
        form=CustomUserCreationForm()                          #changing obj 
        return render(request, "register.html",{"form":form})
    else:
        #submittedform=UserCreationForm(request.POST)
        submittedform=CustomUserCreationForm(request.POST)     #changing obj
        if submittedform.is_valid():
            submittedform.save()
            return HttpResponseRedirect("/login")
        return render(request, "register.html",{"form":submittedform})

def admin(request):
    return render(request,"admin.html",{"products":Product.customManager.all()})