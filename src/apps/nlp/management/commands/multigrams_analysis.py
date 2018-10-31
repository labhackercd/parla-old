from django.core.management.base import BaseCommand
from apps.nlp import multigrams


class Command(BaseCommand):
    help = 'Run multigrams analysis'

    def handle(self, *args, **options):
        multigrams.multigrams_analysis()
