from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('generate-stream', views.StreamGeneratorView.as_view(), name='generate_stream'),
    path('load_categories_sampleproducts',views.Load_Categories_SampleProducts,name='load_categories_sampleproducts')
]

