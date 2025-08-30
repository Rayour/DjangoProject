from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (CategoryDetailView, ContactListView,
                           ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView,
                           ProductUpdateView)
from config.settings import CACHE_TIME

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', cache_page(CACHE_TIME)(ProductDetailView.as_view()), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_list'),
]
