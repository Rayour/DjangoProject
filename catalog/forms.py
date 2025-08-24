from django import forms
from .models import Product


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
