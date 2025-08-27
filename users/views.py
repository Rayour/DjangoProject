from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class CustomUserCreateView(CreateView):
    """Класс представления для создания пользователя"""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")
