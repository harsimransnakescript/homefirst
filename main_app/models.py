from django.db import models

# Create your models here.
class ProductsModel(models.Model):
    group=models.CharField(max_length=1000,null=True,blank=True)
    name=models.CharField(max_length=1000,null=True,blank=True)
    image=models.FileField(null=True,blank=True,upload_to="products/")
    specifications=models.TextField(null=True,blank=True)
    other_info=models.TextField(null=True,blank=True)
    price=models.CharField(max_length=10000,null=True,blank=True)
    
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class SampleProductsModel(models.Model):
    group=models.CharField(max_length=1000,null=True,blank=True)
    name=models.CharField(max_length=1000,null=True,blank=True)
    image=models.FileField(null=True,blank=True,upload_to="sample_products/")
    specifications=models.TextField(null=True,blank=True)
    other_info=models.TextField(null=True,blank=True)
    price=models.CharField(max_length=10000,null=True,blank=True)

class Categories(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name