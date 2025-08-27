from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import CustomUserCreateView, CustomUserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('edit_profile/', CustomUserUpdateView.as_view(), name='edit_profile'),
]
