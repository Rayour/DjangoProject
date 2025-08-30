from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from catalog.models import Category, Contact, Product

from .forms import ProductForm, ProductModeratorForm
from .services import CategoryService, ProductService

PER_PAGE = 4


class ProductListView(ListView):
    """Класс для представления списка продуктов"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод получения контекста"""

        if self.request.GET.get('page'):
            try:
                page = int(self.request.GET.get('page'))
            except Exception:
                page = 1
        else:
            page = 1

        page_count = ProductService.get_page_count(PER_PAGE, 0)
        pages = ProductService.get_pages(page_count)
        page, prev_page, next_page = ProductService.get_prev_next_page(page, page_count)
        products = ProductService.get_product_page_queryset(page, PER_PAGE, 0)
        categories = CategoryService.get_categories_list()

        context = {
            "products": products,
            "categories": categories,
            "category_id": 0,
            "page": page,
            "pages": pages,
            "prev_page": prev_page,
            "next_page": next_page,
            "page_count": page_count
        }

        return context


class ProductDetailView(DetailView):
    """Класс для представления одного продукта"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        """Метод получения объекта продукта"""

        product = super().get_object()
        user = self.request.user
        if not (user == product.owner or user.has_perm(
                "catalog.can_unpublish_product")) and not product.is_published:
            raise PermissionDenied

        return product


class ContactListView(View):
    """Класс для представления контактов"""

    def get(self, request):
        """Метода для обработки GET запросов"""

        contact = Contact.objects.get(id=1)
        context = {
            "contact": contact
        }
        return render(request, 'contacts.html', context=context)

    def post(self, request):
        """Метода для обработки POST запросов"""

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name)
        print(phone)
        print(message)

        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс представления создания продукта"""

    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """При успешном заполнении формы метод добавляет создателя как владельца"""

        user = self.request.user
        if not user.has_perm("catalog.add_product"):
            raise PermissionDenied
        product = form.save()
        product.owner = user
        user.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления редактирования продукта"""

    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        """Метод формирования ссылки для редиректа при успешном редактировании"""

        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        """Метод определения формы редактирования в зависимости от прав пользователя"""

        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления продукта"""

    model = Product
    template_name = "product_delete_confirm.html"
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        """Метод получения объекта продукта"""

        product = super().get_object()
        user = self.request.user
        if not (user == product.owner or user.has_perm("catalog.delete_product")):
            raise PermissionDenied

        return product

    def form_valid(self, form):
        """Метод проверяет наличие прав перед удалением"""

        user = self.request.user
        if not (user == self.object.owner or user.has_perm("catalog.can_delete_product")):
            raise PermissionDenied
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    """Класс представления списка товаров категории"""

    model = Category
    template_name = "home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод получения контекста"""

        if self.request.GET.get('page'):
            try:
                page = int(self.request.GET.get('page'))
            except Exception:
                page = 1
        else:
            page = 1

        if CategoryService.is_category_exist(self.object.pk):
            category_id = self.object.pk
        else:
            category_id = 0

        page_count = ProductService.get_page_count(PER_PAGE, category_id)
        pages = ProductService.get_pages(page_count)
        page, prev_page, next_page = ProductService.get_prev_next_page(page, page_count)
        products = ProductService.get_product_page_queryset(page, PER_PAGE, category_id)
        categories = CategoryService.get_categories_list()

        context = {
            "products": products,
            "categories": categories,
            "category_id": category_id,
            "page": page,
            "pages": pages,
            "prev_page": prev_page,
            "next_page": next_page,
            "page_count": page_count
        }

        return context
