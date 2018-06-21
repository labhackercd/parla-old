from django.core.management.base import BaseCommand
from apps.nlp import tokenizer


class Command(BaseCommand):
    help = 'Pre process all speeches'

    def add_arguments(self, parser):
        parser.add_argument('ngrams', type=int)

    def handle(self, *args, **options):
        tokenizer.process_speeches(ngrams=options['ngrams'])
