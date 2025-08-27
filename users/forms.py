from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя"""

    usable_password = None

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["phone_number"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
        })

    class Meta:
        """Описание формы для создания пользователя"""

        model = CustomUser
        fields = ("email", "username", "phone_number", "password1", "password2")

    def clean_phone_number(self):
        """Метод валидации телефона"""

        phone_number = self.cleaned_data.get("phone_number")

        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Телефон может содержать только цифры")
        return phone_number


class CustomUserChangeForm(forms.ModelForm):
    """Форма редактирования пользователя"""

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["phone_number"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["country"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["avatar"].widget.attrs.update({
            "class": "form-control",
        })

    class Meta:
        """Описание формы для редактирования пользователя"""

        model = User
        fields = ("first_name", "last_name", "country", "phone_number", "avatar")

    def clean_phone_number(self):
        """Метод валидации телефона"""

        phone_number = self.cleaned_data.get("phone_number")

        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Телефон может содержать только цифры")
        return phone_number
