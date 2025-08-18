from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Функция рендера домашней страницы"""

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
    return render(request, 'contacts.html')
