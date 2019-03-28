from django.core.management.base import BaseCommand
from apps.data import fetch, models
from django.db import transaction
import click


class Command(BaseCommand):
    help = 'Update speeches phases'

    def handle(self, *args, **options):
        speeches = models.Speech.objects.all().order_by('date')
        with click.progressbar(speeches) as bar:
            with transaction.atomic():
                for speech in bar:
                    speech.original_phase = speech.phase
                    speech.phase = fetch.PHASE_RELATION[speech.phase]
                    speech.save()
