from django.core.management.base import BaseCommand
from apps.nlp import multigrams


class Command(BaseCommand):
    help = 'Run multigrams analysis'

    def add_arguments(self, parser):
        parser.add_argument('use_unigram', type=int)

    def handle(self, *args, **options):
        use_unigram = bool(options['use_unigram'])
        multigrams.multigrams_analysis(use_unigram=use_unigram)
