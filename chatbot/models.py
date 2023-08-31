from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Patient_Query(models.Model):
    question = models.CharField(max_length=300)
    
    def __str__(self) -> str:
        return self.question

class Products(models.Model): 
    product_group = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    product_features = models.TextField()
    product_specifications = models.TextField()
    product_more_information = models.TextField()

    def __str__(self):
        return self.product_name