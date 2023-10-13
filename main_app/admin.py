from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ProductsModel)
admin.site.register(SampleProductsModel)
admin.site.register(Categories)
admin.site.register(OrderSample)
admin.site.register(AuthorizationStatus)
admin.site.register(FormModel)
admin.site.register(TicketComment)