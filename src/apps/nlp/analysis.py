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


def get_phases(qs):
    return sorted(set(list(qs.values_list('phase', flat=True))))


def decision_tree_analysis_by_phase():
    secho('\nProcessing speeches from ALL phases')
    speech_list = data.Speech.objects.all().order_by('date')
    decision_tree_analysis(speech_list, 'TODAS')
    for phase in get_phases(speech_list):
        secho('\nFiltering speeches from phase: {}'.format(phase))
        filtred_speeches = speech_list.filter(phase=phase)
        decision_tree_analysis(filtred_speeches, phase)


def decision_tree_analysis(speeches, phase):
    for date in months(speeches):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        queryset = speeches.filter(
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
                    algorithm='decision_tree',
                    phase=phase
                )[0]

                analysis.data = final_dict
                analysis.save()


def translate_stem(stem, stems_dict):
    stem_words = stem.split(' ')
    words = []
    for word in stem_words:
        stem_list = stems_dict.get(word)
        words.append(max(stem_list, key=stem_list.count))

    return ' '.join(words)


def multigram_analysis_by_phase(use_unigram=True):
    secho('\nProcessing speeches from ALL phases')
    speech_list = data.Speech.objects.all().order_by('date')
    multigrams_analysis(use_unigram, speech_list, 'TODAS')
    for phase in get_phases(speech_list):
        secho('\nFiltering speeches from phase: {}'.format(phase))
        filtred_speeches = speech_list.filter(phase=phase)
        multigrams_analysis(use_unigram, filtred_speeches, phase)


def multigrams_analysis(use_unigram, speeches, phase):
    if use_unigram:
        algorithm = nlp.Analysis.MULTIGRAM_BOW_WITH_UNIGRAM
    else:
        algorithm = nlp.Analysis.MULTIGRAM_BOW_WITHOUT_UNIGRAM

    for date in months(speeches):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        queryset = speeches.filter(
            date__gte=start_date,
            date__lte=end_date
        )

        final_dict = {}

        with progressbar(queryset) as bar:
            for speech in bar:
                tokens, stems_dict = multigrams.get_tokens(speech.content)
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
                trigrams = multigrams.ngrams_by_limit(trigram_tokens,
                                                      3, limit)

                if trigrams:
                    stop_trigrams = list(list(zip(*trigrams))[0])

                bigram_tokens = multigrams.clean_tokens(
                    tokens, stop_fivegrams, stop_quadgrams, stop_trigrams
                )

                bigrams = multigrams.ngrams_by_limit(bigram_tokens,
                                                     2, limit)

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
                    word_token = translate_stem(' '.join(token[0]), stems_dict)
                    token_data = final_dict.get(word_token, {})
                    authors = token_data.get('authors', {})
                    author_data = authors.get(speech.author.id, {})
                    texts = author_data.get('texts', [])
                    texts.append({speech.id: token[1]})

                    author_data['texts_count'] = len(texts)
                    author_data['texts'] = texts
                    authors[speech.author.id] = author_data
                    token_data['authors'] = authors
                    token_data['authors_count'] = len(authors)
                    final_dict[word_token] = token_data

            if len(final_dict) > 0:
                analysis = nlp.Analysis.objects.get_or_create(
                    start_date=start_date,
                    end_date=end_date,
                    algorithm=algorithm,
                    phase=phase
                )[0]

                analysis.data = final_dict
                analysis.save()
