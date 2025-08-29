from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from catalog.models import Contact, Product

from .forms import ProductForm, ProductModeratorForm


class ProductListView(ListView):
    """Класс для представления списка продуктов"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод получения контекста"""

        PER_PAGE = 4

        if self.request.GET.get('page'):
            try:
                page = int(self.request.GET.get('page'))
            except Exception:
                page = 1
        else:
            page = 1

        products_count = Product.objects.filter(is_published=True).count()
        print(products_count)

        if products_count % PER_PAGE:
            page_count = products_count // PER_PAGE + 1
        else:
            page_count = products_count // PER_PAGE

        pages = [i + 1 for i in range(page_count)]

        if 1 < page < page_count:
            prev_page = page - 1
            next_page = page + 1
        elif page <= 1:
            page = 1
            prev_page = 1
            next_page = page + 1
        else:
            page = page_count
            prev_page = page - 1
            next_page = page_count

        start = page * PER_PAGE - PER_PAGE
        stop = start + PER_PAGE
        products = Product.objects.filter(is_published=True).order_by("created_at")[start:stop]

        context = {
            "products": products,
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
                "catalog.can_unpublish_product")) and product.is_published == False:
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
        if not user.has_perm("catalog.can_add_product"):
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
        if not (user == product.owner or user.has_perm("catalog.can_delete_product")):
            raise PermissionDenied

        return product

    def form_valid(self, form):
        """Метод проверяет наличие прав перед удалением"""

        user = self.request.user
        if not (user == self.object.owner or user.has_perm("catalog.can_delete_product")):
            raise PermissionDenied
        return super().form_valid(form)
