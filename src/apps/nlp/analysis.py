from django.db.models import Q
from django.db import transaction
from dateutil.rrule import rrule, MONTHLY
from calendar import monthrange
from click import progressbar, secho
import datetime

from apps.nlp import models as nlp
from apps.data import models as data


def date_filter(start_date, end_date):
    return Q(speech__date__gte=start_date, speech__date__lte=end_date)


def months(queryset):
    start_date = queryset.first().date
    end_date = queryset.last().date
    return rrule(MONTHLY, dtstart=start_date, until=end_date)


def ngrams_analysis(ngrams=1, use_indexes=False):
    speech_list = data.Speech.objects.all().order_by('date')
    if ngrams == 1:
        algorithm = nlp.Analysis.UNIGRAM_BOW
    else:
        algorithm = nlp.Analysis.BIGRAM_BOW

    for date in months(speech_list):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        queryset = nlp.SpeechToken.objects.filter(
            token__ngrams=ngrams,
            use_indexes=use_indexes,
            speech__date__gte=start_date,
            speech__date__lte=end_date
        )
        final_dict = {}

        with progressbar(queryset) as bar:
            for speech_token in bar:
                token_data = final_dict.get(speech_token.token.stem, {})
                authors = token_data.get('authors', {})
                author_data = authors.get(speech_token.speech.author.id, {})
                texts = author_data.get('texts', [])

                texts.append(
                    {speech_token.speech.id: speech_token.occurrences}
                )

                author_data['texts_count'] = len(texts)
                author_data['texts'] = texts
                authors[speech_token.speech.author.id] = author_data
                token_data['authors'] = authors
                token_data['authors_count'] = len(authors)
                final_dict[speech_token.token.stem] = token_data

            if len(final_dict) > 0:
                analysis = nlp.Analysis.objects.get_or_create(
                    start_date=start_date,
                    end_date=end_date,
                    use_indexes=use_indexes,
                    algorithm=algorithm
                )[0]

                analysis.data = final_dict
                analysis.save()
