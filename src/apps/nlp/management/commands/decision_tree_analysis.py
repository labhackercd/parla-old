from django.core.management.base import BaseCommand
from apps.nlp import analysis


class Command(BaseCommand):
    help = 'Run naive bayes thematic analysis'

    def handle(self, *args, **options):
        analysis.decision_tree_analysis_by_phase()
