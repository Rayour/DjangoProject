import os.path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from unicodedata import category

from catalog.models import Contact, Product, Category


def home(request):
    """Функция рендера домашней страницы"""

    PER_PAGE = 4

    if request.GET.get('page'):
        try:
            page = int(request.GET.get('page'))
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
    print(context)

    return render(request, 'home.html', context=context)


def product_detail(request, product_id):
    """Функция рендера домашней страницы"""

    product = Product.objects.get(id=product_id)
    context = {"product": product}

    return render(request, 'product_detail.html', context=context)


def contacts(request):
    """Функция обработки запросов страницы контактов"""

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name)
        print(phone)
        print(message)

        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    contact = Contact.objects.get(id=1)
    context = {
        "contact": contact
    }
    return render(request, 'contacts.html', context=context)


def add_product(request):
    """Функция обработки запросов страницы контактов"""

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category.objects.get(id=request.POST.get('category'))
        price = request.POST.get('price')
        if 'image' in request.FILES:
            print("123")
            image = request.FILES['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, 'wb+') as file:
                for chunk in image.chunks():
                    file.write(chunk)
            product = Product.objects.create(name=name, description=description, price=price, image=image.name,
                                             category=category)
        else:
            product = Product.objects.create(name=name, description=description, price=price, category=category)
        context = {
            'product': product
        }

        return render(request, 'success.html', context=context)
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'add_product.html', context=context)
