from django.db import models
from auth_app.models import User
from django.utils import timezone

# Create your models here.
class ProductsModel(models.Model):
    group=models.CharField(max_length=1000,null=True,blank=True)
    name=models.CharField(max_length=1000,null=True,blank=True)
    image=models.FileField(null=True,blank=True,upload_to="products/")
    specifications=models.TextField(null=True,blank=True)
    other_info=models.TextField(null=True,blank=True)
    price=models.CharField(max_length=10000,null=True,blank=True)
    
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='products',null=True,blank=True)

    def __str__(self):
        return self.name

class SampleProductsModel(models.Model):
    group=models.CharField(max_length=1000,null=True,blank=True)
    name=models.CharField(max_length=1000,null=True,blank=True)
    image=models.FileField(null=True,blank=True,upload_to="sample_products/")
    specifications=models.TextField(null=True,blank=True)
    other_info=models.TextField(null=True,blank=True)
    price=models.CharField(max_length=10000,null=True,blank=True)
    
    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
    
class OrderSample(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    sample_item =  models.ForeignKey(SampleProductsModel, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=255, choices=[
        ('Pick Up in Office', 'Pick Up in Office'),
        ('Home Delivery', 'Home Delivery'),
    ])
    shipping_address = models.TextField(null=True,blank=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    mobile_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.first_name} {self.last_name}"
    
    
class AuthorizationStatus(models.Model):
    task = models.FileField(upload_to="task/")
    starting_date = models.DateField()
    ending_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Expired', 'Expired')])

    def save(self, *args, **kwargs):
        if self.ending_date < timezone.now().date() and self.status == 'Active':
            self.status = 'Expired'
        super().save(*args, **kwargs)

    



