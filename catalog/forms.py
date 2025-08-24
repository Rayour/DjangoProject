from django import forms
from django.core.exceptions import ValidationError
from .models import Product

BLACK_LIST = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар"
        ]


class ProductForm(forms.ModelForm):
    """Класс формы для создания продукта"""

    class Meta:
        """Описание формы для создания продукта"""

        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["description"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["image"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["category"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["price"].widget.attrs.update({
            "class": "form-control",
        })

    def clean_name(self):
        """Метод валидации названия. Запрет на слова из черного списка"""

        name = self.cleaned_data.get("name")

        for word in BLACK_LIST:
            if word in name.lower():
                raise ValidationError(f'Вы не можете использовать слово "{word}" в названии продукта.')
        return name

    def clean_description(self):
        """Метод валидации описания. Запрет на слова из черного списка"""

        description = self.cleaned_data.get("description")

        for word in BLACK_LIST:
            if word in description.lower():
                raise ValidationError(f'Вы не можете использовать слово "{word}" в описании продукта.')
        return description

    def clean_price(self):
        """Метод валидации цены. Цена должна быть больше нуля"""

        price = self.cleaned_data.get("price")

        if price <= 0:
            raise ValidationError("Цена продукта на может быть меньше или равной 0")
        return price
