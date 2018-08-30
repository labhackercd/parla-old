from django.core.management.base import BaseCommand
from apps.nlp import analysis


class Command(BaseCommand):
    help = 'Run n-grams author Analysis'

    def add_arguments(self, parser):
        parser.add_argument('ngrams', type=int)
        parser.add_argument('use_indexes', type=bool)

    def handle(self, *args, **options):
        ngrams = options['ngrams']
        use_indexes = options['use_indexes']
        analysis.ngrams_analysis(ngrams=ngrams, use_indexes=use_indexes)
