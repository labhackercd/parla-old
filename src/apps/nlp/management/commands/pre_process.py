from django.core.management.base import BaseCommand
from apps.nlp import tokenizer, models


class Command(BaseCommand):
    help = 'Pre process all speeches'

    def add_arguments(self, parser):
        parser.add_argument('ngrams', type=int)

    def handle(self, *args, **options):
        ngrams = options['ngrams']
        if ngrams == 1:
            algorithm = models.Analysis.UNIGRAM_BOW
        else:
            algorithm = models.Analysis.BIGRAM_BOW

        tokenizer.process_speeches(algorithm, ngrams=ngrams)
