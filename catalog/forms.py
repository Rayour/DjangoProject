from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

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

    def clean_image(self):
        """Метод валидации изображения товара.
        Проверка формата (jpeg, png) и размера (5Mb max)"""

        image = self.cleaned_data.get("image")

        if image:
            try:
                img = Image.open(image.file)
                img_format = img.format

                allowed_formats = ['PNG', 'JPEG']

                if img_format not in allowed_formats:
                    raise forms.ValidationError("Необходимо загрузить фото в формате .png или .jpeg")
                image.file.seek(0)

            except Exception:
                raise forms.ValidationError("Загруженный файл не является изображением")

            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Файл слишком тяжелый. Максимальный допустимый вес: 5 Mb.")
        return image


class ProductModeratorForm(forms.ModelForm):
    """Класс формы для модератора продукта"""

    class Meta:
        """Описание формы для модератора продукта"""

        model = Product
        fields = ["is_published"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(ProductModeratorForm, self).__init__(*args, **kwargs)

        self.fields["is_published"].widget.attrs.update({
            "class": "form-check",
        })

    def clean_is_published(self):
        """Метод проверяет, что продукт снимается с публикации при редактировании"""

        is_published = self.cleaned_data.get("is_published")

        if is_published:
            raise ValidationError("Вы можете только снять продукт с публикации, но не опубликовать его.")
        return is_published
