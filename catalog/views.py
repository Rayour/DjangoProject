from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Contact, Product


def home(request):
    """Функция рендера домашней страницы"""

    products = Product.objects.order_by("created_at")
    context = {"products": products[:5]}
    print(context)
    return render(request, 'home.html')


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
    print(contact)
    return render(request, 'contacts.html')
