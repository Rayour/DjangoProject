from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import DEFAULT_FROM_EMAIL

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()

class CustomUserCreateView(CreateView):
    """Класс представления для создания пользователя"""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления для редактирования пользователя"""

    model = User
    template_name = "edit_profile.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        """Метод получения пользователя"""
        return self.request.user
