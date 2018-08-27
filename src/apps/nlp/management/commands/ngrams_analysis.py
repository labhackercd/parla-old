from django.core.management.base import BaseCommand
from apps.nlp import analysis


class Command(BaseCommand):
    help = 'Run n-grams author Analysis'

    def add_arguments(self, parser):
        parser.add_argument('ngrams', type=int)

    def handle(self, *args, **options):
        ngrams = options['ngrams']
        analysis.ngrams_analysis(ngrams=ngrams)
