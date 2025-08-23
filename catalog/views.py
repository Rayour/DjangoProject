import os.path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View

from catalog.models import Contact, Product, Category


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

        products_count = Product.objects.count()
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
        products = Product.objects.order_by("created_at")[start:stop]

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


class ProductCreateView(CreateView):
    """Класс представления создания продукта"""

    model = Product
    fields = ["name", "description", "category", "price", "image"]
    template_name = "add_product.html"
    success_url = reverse_lazy('catalog:home')
