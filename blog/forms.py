from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    """Класс формы для создания статьи"""

    class Meta:
        """Описание формы для создания статьи"""

        model = Article
        fields = ["title", "content", "image", "is_published"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["content"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["image"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["is_published"].widget.attrs.update({
            "class": "form-check",
        })
