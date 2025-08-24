from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import Article


class Command(BaseCommand):
    help = 'Delete all data and load test data from fixture'

    def handle(self, *args, **kwargs):

        Article.objects.all().delete()

        call_command('loaddata', 'articles_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded articles from fixture'))
