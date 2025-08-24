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

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
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
        name = self.cleaned_data.get("name")

        for word in BLACK_LIST:
            if word in name.lower():
                raise ValidationError(f'Вы не можете использовать слово "{word}" в названии продукта.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")

        for word in BLACK_LIST:
            if word in description.lower():
                raise ValidationError(f'Вы не можете использовать слово "{word}" в описании продукта.')
        return description
