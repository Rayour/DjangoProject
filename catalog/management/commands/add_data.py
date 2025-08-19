from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Delete all data and load test data from fixture'

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'categories_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded categories from fixture'))

        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded products from fixture'))
