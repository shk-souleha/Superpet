from django.db import models
from autoslug import AutoSlugField

#------------------------------------------------------------------
#               CATEGORY MODEL
#------------------------------------------------------------------
class Category(models.Model):
    category_name=models.CharField(max_length=100,null=False)
    category_slug=AutoSlugField(populate_from="category_name",unique=True)

    def __str__(self):
        return self.category_name


#------------------------------------------------------------------
#               PRODUCT CUSTOM MANAGER
#------------------------------------------------------------------
class ProductCustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    #Method of royal canin
    def royalCanin(self):
        return super().get_queryset().filter(product_brand="Royal Canin")

    #method for drools
    def drools(self):
        return super().get_queryset().filter(product_brand="Drools")
    



# Create your models here.
# step 1 : create class which inherits Model class from models

#------------------------------------------------------------------
#               PRODUCT MODEL
#------------------------------------------------------------------
class Product(models.Model):
    prodcuct_name=models.CharField(max_length=100,null=False)
    product_description=models.TextField(default="product description")
    product_price=models.PositiveIntegerField(default=0)
    product_image=models.ImageField(upload_to="products/")
    product_brand=models.CharField(max_length=100,default="superpet")
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

#   changing manager name from objects to prodManager 
    prodManager=models.Manager()

    #changing manager name from customManager to ProductCustomManager
    customManager=ProductCustomManager()

#   always write __str__ in the last 
    def __str__(self):
        return self.prodcuct_name


    

