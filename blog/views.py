from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Article

from .forms import ArticleForm


class BlogListView(LoginRequiredMixin, ListView):
    """Класс представления списка статей блога"""

    model = Article
    template_name = "blog.html"
    context_object_name = "articles"

    def get_queryset(self):
        """Метод получения списка опубликованных статей"""

        articles = Article.objects.filter(is_published=True)
        return articles


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Класс представления создания статьи блога"""

    model = Article
    template_name = "add_edit_article.html"
    form_class = ArticleForm
    success_url = reverse_lazy('blog:article_list')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления редактирования статьи блога"""

    model = Article
    template_name = "add_edit_article.html"
    form_class = ArticleForm

    def get_success_url(self):
        """Метод формирования ссылки для редиректа при успешном редактировании"""

        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Класс представления детальной информации о статье"""

    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        """Метод получения объекта статьи"""

        article = super().get_object()
        article.view_count += 1
        article.save()

        return article


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления статьи блога"""

    model = Article
    template_name = "article_delete_confirm.html"
    success_url = reverse_lazy('blog:article_list')
