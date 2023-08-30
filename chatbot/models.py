from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Patient_Query(models.Model):
    question = models.CharField(max_length=300)
    
    def __str__(self) -> str:
        return self.question

class Products(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="products/")
    
    def __str__(self):
        return self.product_name
    