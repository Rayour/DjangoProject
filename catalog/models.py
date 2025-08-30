from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Модель категории товара"""

    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", null=True, blank=True,
                                   help_text="Введите описание категории товаров")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта категории"""

        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", null=True, blank=True, help_text="Введите описание товара")
    image = models.ImageField(upload_to="media/", null=True, blank=True, verbose_name="Изображение",
                              help_text="Загрузите изображение товара")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(verbose_name="Цена", help_text="Укажите стоимость единицы товара")
    is_published = models.BooleanField(verbose_name="Опубликован?", null=True, blank=True, default=True,
                                       help_text="Только опубликованные продукты отображаются в каталоге")
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="products")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта продукта"""

        return f"{self.name}. Цена: {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "price", "created_at"]
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]


class Contact(models.Model):
    """Модель контакта"""

    country = models.CharField(max_length=30, verbose_name="Страна")
    tin = models.CharField(max_length=20, verbose_name="ИНН")
    address = models.TextField(verbose_name="Адрес")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта категории"""

        return f"Страна: {self.country}, ИНН: {self.tin}, Адрес: {self.address}"

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = ["country", "tin"]
