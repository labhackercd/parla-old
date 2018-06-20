from django.core.management.base import BaseCommand
from django.conf import settings
from apps.data import fetch


class Command(BaseCommand):
    help = 'Import data from Babel'

    def handle(self, *args, **options):
        print('Getting data from Babel')
        json_data = fetch.get_json_data('manifestations',
                                        settings.BABEL_SPEECH_TYPE_ID)
        print('Processing speeches...')
        speeches = fetch.create_speeches(json_data)
        print('{} speeches saved!'.format(len(speeches)))
