from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
