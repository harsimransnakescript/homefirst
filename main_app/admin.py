from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ProductsModel)
admin.site.register(SampleProductsModel)
admin.site.register(Categories)
admin.site.register(Requester)
admin.site.register(Sample)
admin.site.register(SampleRequest)
admin.site.register(SampleRequestHistory)