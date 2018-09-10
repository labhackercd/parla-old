from django.db.models import Q
from textblob.classifiers import NaiveBayesClassifier as Classifier
from dateutil.rrule import rrule, MONTHLY
from calendar import monthrange
from click import progressbar, secho
import datetime

from apps.nlp import models as nlp, naive_bayes, cache
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


def get_naive_bayes_classifier():
    return Classifier(
        naive_bayes.get_initial_trainset(),
        feature_extractor=naive_bayes.extract
    )


def naive_bayes_analysis():
    speech_list = data.Speech.objects.all().order_by('date')
    print('Training classifier...')
    classifier = cache.load_from_cache(
        'classifier', initial_value_method=get_naive_bayes_classifier
    )
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
                if speech.indexes:
                    indexes = speech.indexes.replace('.', ',')
                    indexes = indexes.split(',')

                    for index in indexes:
                        prob_dist = classifier.prob_classify(index)
                        label = prob_dist.max()
                        if prob_dist.prob(label) > 0.5:
                            token_data = final_dict.get(label, {})
                            authors = token_data.get('authors', {})
                            author_data = authors.get(speech.author.id, {})
                            texts = author_data.get('texts', [])
                            texts.append({speech.id: 1})

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
                    use_indexes=True,
                    algorithm='naive_bayes'
                )[0]

                analysis.data = final_dict
                analysis.save()
