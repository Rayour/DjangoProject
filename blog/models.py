from django.db import models


class Article(models.Model):
    """Модель статьи блога"""

    title = models.CharField(max_length=300, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое", help_text="Введите текст статьи")
    image = models.ImageField(upload_to="media/", null=True, blank=True, verbose_name="Превью",
                              help_text="Загрузите изображение для превью статьи")
    is_published = models.BooleanField(verbose_name="Опубликована?", default=False,
                                       help_text="Признак публикации статьи")
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта статьи"""

        return f"{self.title}. Количество просмотров: {self.view_count}"

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["title", "view_count", "created_at"]
