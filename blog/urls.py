from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogUpdateView, BlogDetailView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='article_list'),
    path('add_article/', BlogCreateView.as_view(), name='article_create'),
    path('edit_article/<int:pk>/', BlogUpdateView.as_view(), name='article_edit'),
    path('article_detail/<int:pk>/', BlogDetailView.as_view(), name='article_detail'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='article_delete')
]
