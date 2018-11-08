from django.db.models import Q
from textblob.classifiers import NaiveBayesClassifier as Classifier
from dateutil.rrule import rrule, MONTHLY
from calendar import monthrange
from click import progressbar, secho
import datetime

from apps.nlp import models as nlp, decision_tree, cache
from apps.data import models as data


def date_filter(start_date, end_date):
    return Q(speech__date__gte=start_date, speech__date__lte=end_date)


def months(queryset):
    start_date = queryset.first().date
    end_date = queryset.last().date
    return rrule(MONTHLY, dtstart=start_date, until=end_date)


def decision_tree_analysis():
    speech_list = data.Speech.objects.all().order_by('date')
    for date in months(speech_list):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        queryset = speech_list.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        final_dict = {}
        with progressbar(queryset) as bar:
            for speech in bar:
                classes = decision_tree.classify_speech(
                    speech.original,
                    normalize=False
                )
                for label, occurrences in classes.most_common():
                    token_data = final_dict.get(label, {})
                    authors = token_data.get('authors', {})
                    author_data = authors.get(speech.author.id, {})
                    texts = author_data.get('texts', [])
                    texts.append({speech.id: occurrences})

                    author_data['texts_count'] = len(texts)
                    author_data['texts'] = texts
                    authors[speech.author.id] = author_data
                    token_data['authors'] = authors
                    token_data['authors_count'] = len(authors)
                    final_dict[label] = token_data

            if len(final_dict) > 0:
                analysis = nlp.Analysis.objects.get_or_create(
                    start_date=start_date,
                    end_date=end_date,
                    algorithm='decision_tree'
                )[0]

                analysis.data = final_dict
                analysis.save()
