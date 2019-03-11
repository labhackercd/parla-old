from django.core.management.base import BaseCommand
from apps.data import fetch, models
from calendar import monthrange
from dateutil.rrule import rrule, MONTHLY
import datetime
import click


class Command(BaseCommand):
    help = 'Import data from Babel'

    def handle(self, *args, **options):
        last_speech = models.Speech.objects.all().order_by('timestamp').last()
        if last_speech:
            initial_date = last_speech.date
        else:
            initial_date = datetime.date(2015, 1, 1)

        end_date = datetime.date.today()
        months = rrule(MONTHLY, dtstart=initial_date, until=end_date)
        for date in months:
            days = monthrange(date.year, date.month)[1]
            final_date = datetime.date(date.year, date.month, days)

            click.echo('Fetch data from {} to {}'.format(
                date.strftime('%d/%m/%Y'),
                final_date.strftime('%d/%m/%Y')
            ))

            data = fetch.fetch_data(
                date.strftime('%d/%m/%Y'),
                final_date.strftime('%d/%m/%Y')
            )

            fetch.create_speeches(data)
