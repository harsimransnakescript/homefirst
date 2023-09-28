from django.db import models
from auth_app.models import User

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
    shipping_address = models.TextField(blank=True, null=True)
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
    
    
class Requester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model for authentication
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Sample(models.Model):
    name = models.CharField(max_length=255)
    available_quantity = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=255)
    product_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class SampleRequest(models.Model):
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)
    status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=status_choices)
    quantity = models.PositiveIntegerField()
    shipping_address = models.TextField()
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sample Request #{self.pk}"

class SampleRequestHistory(models.Model):
    sample_request = models.ForeignKey(SampleRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SampleRequest.status_choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.sample_request} - {self.status}"