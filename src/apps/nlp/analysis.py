from django.db.models import Q
from dateutil.rrule import rrule, MONTHLY
from calendar import monthrange
from click import progressbar, secho
import datetime

from apps.nlp import models as nlp, decision_tree, multigrams, stopwords
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
                    speech.content,
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


def multigrams_analysis(use_unigram=True):
    speech_list = data.Speech.objects.all().order_by('date')

    if use_unigram:
        algorithm = nlp.Analysis.MULTIGRAM_BOW_WITH_UNIGRAM
    else:
        algorithm = nlp.Analysis.MULTIGRAM_BOW_WITHOUT_UNIGRAM

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
                tokens = multigrams.get_tokens(speech.content)
                limit = 2
                stop_fivegrams = []
                stop_quadgrams = []
                stop_trigrams = []
                stop_bigrams = []
                fivegrams = multigrams.ngrams_by_limit(tokens, 5, limit)

                if fivegrams:
                    stop_fivegrams = list(list(zip(*fivegrams))[0])

                quadgram_tokens = multigrams.clean_tokens(tokens,
                                                          stop_fivegrams)
                quadgrams = multigrams.ngrams_by_limit(quadgram_tokens,
                                                       4, limit)

                if quadgrams:
                    stop_quadgrams = list(list(zip(*quadgrams))[0])

                trigram_tokens = multigrams.clean_tokens(tokens,
                                                         stop_fivegrams,
                                                         stop_quadgrams)
                trigrams = multigrams.ngrams_by_limit(trigram_tokens, 3, limit)

                if trigrams:
                    stop_trigrams = list(list(zip(*trigrams))[0])

                bigram_tokens = multigrams.clean_tokens(
                    tokens, stop_fivegrams, stop_quadgrams, stop_trigrams
                )

                bigrams = multigrams.ngrams_by_limit(bigram_tokens, 2, limit)

                if bigrams:
                    stop_bigrams = list(list(zip(*bigrams))[0])

                onegram_tokens = multigrams.clean_tokens(
                    tokens, stop_fivegrams,
                    stop_quadgrams, stop_trigrams,
                    stop_bigrams, stopwords.ONEGRAM_STOPWORDS
                )
                onegrams = multigrams.ngrams_by_limit(onegram_tokens, 1)

                if use_unigram:
                    result_tokens = (onegrams + bigrams + trigrams +
                                     quadgrams + fivegrams)
                else:
                    result_tokens = (bigrams + trigrams + quadgrams +
                                     fivegrams)

                for token in result_tokens:
                    token_data = final_dict.get(' '.join(token[0]), {})
                    authors = token_data.get('authors', {})
                    author_data = authors.get(speech.author.id, {})
                    texts = author_data.get('texts', [])
                    texts.append({speech.id: token[1]})

                    author_data['texts_count'] = len(texts)
                    author_data['texts'] = texts
                    authors[speech.author.id] = author_data
                    token_data['authors'] = authors
                    token_data['authors_count'] = len(authors)
                    final_dict[' '.join(token[0])] = token_data

            if len(final_dict) > 0:
                analysis = nlp.Analysis.objects.get_or_create(
                    start_date=start_date,
                    end_date=end_date,
                    algorithm=algorithm
                )[0]

                analysis.data = final_dict
                analysis.save()
