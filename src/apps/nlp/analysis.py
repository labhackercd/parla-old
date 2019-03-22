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


def get_states(qs):
    return sorted(set(list(qs.values_list('author__state', flat=True))))


def get_parties(qs):
    return sorted(set(list(qs.values_list('author__party', flat=True))))


def decision_tree_analysis_by_phase():
    secho('\nProcessing speeches from ALL phases')
    speech_list = data.Speech.objects.exclude(
        content__startswith='Ata'
    ).filter(author__author_type='Deputado').order_by('date')
    decision_tree_analysis(speech_list)

    secho('\nProcessing speeches from FEMALE authors')
    decision_tree_analysis(speech_list.filter(author__gender='F'), gender='F')

    secho('\nProcessing speeches from MALE authors')
    decision_tree_analysis(speech_list.filter(author__gender='M'), gender='M')

    for phase in get_phases(speech_list):
        if phase:
            secho('\nFiltering speeches from phase: {}'.format(phase))
            filtred_speeches = speech_list.filter(phase=phase)
            decision_tree_analysis(filtred_speeches, phase=phase)

    for state in get_states(speech_list):
        if state:
            secho('\nFiltering speeches from state: {}'.format(state))
            filtred_speeches = speech_list.filter(author__state=state)
            decision_tree_analysis(filtred_speeches, state=state)

    for party in get_parties(speech_list):
        if party:
            secho('\nFiltering speeches from party: {}'.format(party))
            filtred_speeches = speech_list.filter(author__party=party)
            decision_tree_analysis(filtred_speeches, party=party)


def decision_tree_analysis(speeches, phase=None, gender=None,
                           state=None, party=None):
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
                    phase=phase,
                    gender=gender,
                    state=state,
                    party=party,
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
    speech_list = data.Speech.objects.exclude(
        content__startswith='Ata'
    ).filter(author__author_type='Deputado').order_by('date')
    multigrams_analysis(use_unigram, speech_list)

    secho('\nProcessing speeches from FEMALE authors')
    multigrams_analysis(use_unigram, speech_list.filter(author__gender='F'),
                        gender='F')

    secho('\nProcessing speeches from MALE authors')
    multigrams_analysis(use_unigram, speech_list.filter(author__gender='M'),
                        gender='M')

    for phase in get_phases(speech_list):
        if phase:
            secho('\nFiltering speeches from phase: {}'.format(phase))
            filtred_speeches = speech_list.filter(phase=phase)
            multigrams_analysis(use_unigram, filtred_speeches, phase=phase)

    for state in get_states(speech_list):
        if state:
            secho('\nFiltering speeches from state: {}'.format(state))
            filtred_speeches = speech_list.filter(author__state=state)
            multigrams_analysis(use_unigram, filtred_speeches, state=state)

    for party in get_parties(speech_list):
        if party:
            secho('\nFiltering speeches from party: {}'.format(party))
            filtred_speeches = speech_list.filter(author__party=party)
            multigrams_analysis(use_unigram, filtred_speeches, party=party)


def multigrams_analysis(use_unigram, speeches, phase=None, gender=None,
                        state=None, party=None):
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
                stop_trigrams = []
                stop_bigrams = []

                trigram_tokens = multigrams.clean_tokens(tokens)
                trigrams = multigrams.ngrams_by_limit(trigram_tokens,
                                                      3, limit)

                if trigrams:
                    stop_trigrams = list(list(zip(*trigrams))[0])

                bigram_tokens = multigrams.clean_tokens(tokens, stop_trigrams)

                bigrams = multigrams.ngrams_by_limit(bigram_tokens,
                                                     2, limit)

                if bigrams:
                    stop_bigrams = list(list(zip(*bigrams))[0])

                onegram_tokens = multigrams.clean_tokens(
                    tokens, stop_trigrams,
                    stop_bigrams, stopwords.ONEGRAM_STOPWORDS
                )
                onegrams = multigrams.ngrams_by_limit(onegram_tokens, 1)

                if use_unigram:
                    result_tokens = (onegrams + bigrams + trigrams)
                else:
                    result_tokens = (bigrams + trigrams)

                for token in result_tokens:
                    valid_tokens = []
                    for idx in range(len(token[0])):
                        if idx < len(token[0]) - 1:
                            if token[0][idx] != token[0][idx + 1]:
                                valid_tokens.append(token[0][idx])
                        else:
                            valid_tokens.append(token[0][idx])

                    word_token = translate_stem(' '.join(valid_tokens),
                                                stems_dict)
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
                    phase=phase,
                    gender=gender,
                    state=state,
                    party=party,
                )[0]

                analysis.data = final_dict
                analysis.save()
