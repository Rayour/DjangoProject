from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product')
]
