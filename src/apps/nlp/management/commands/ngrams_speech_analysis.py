from django.core.management.base import BaseCommand
from apps.nlp import analysis


class Command(BaseCommand):
    help = 'Run n-grams token Analysis'

    def add_arguments(self, parser):
        parser.add_argument('ngrams', type=int)

    def handle(self, *args, **options):
        ngrams = options['ngrams']
        analysis.ngrams_speech_analysis(ngrams=ngrams)
