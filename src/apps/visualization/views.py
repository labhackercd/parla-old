from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.nlp import models
from apps.data import models as data_models
from apps.data.models import Speech
from datetime import datetime
from collections import Counter
from django.http import JsonResponse
import re


def get_date_filter(start_field, end_field, request):
    date_filter = Q()
    initial_date = request.GET.get('initial_date', None)
    final_date = request.GET.get('final_date', None)

    if initial_date:
        initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        kwargs = {"{}__gte".format(start_field): initial_date}
        date_filter = date_filter & Q(**kwargs)

    if final_date:
        final_date = datetime.strptime(final_date, '%Y-%m-%d')
        kwargs = {"{}__lte".format(end_field): final_date}
        date_filter = date_filter & Q(**kwargs)

    return date_filter


def get_algorithm_filter(request):
    algorithm = request.GET.get('algorithm', None)
    if algorithm:
        return Q(algorithm=algorithm)
    else:
        return Q(algorithm='unigram_bow')


def tokens(request):
    date_filter = get_date_filter('start_date', 'end_date', request)
    analyses = models.Analysis.objects.filter(
        date_filter &
        get_algorithm_filter(request)
    )
    bow = Counter()
    for analysis in analyses:
        for stem, token_data in analysis.data.items():
            bow.update({stem: token_data['authors_count']})

    tokens = models.Token.objects.all()
    final_dict = []
    for i, stem in enumerate(bow.most_common(20)):
        token = tokens.get(stem=stem[0])

        obj = {}
        obj['id'] = token.id
        obj['token'] = token.original
        obj['stem'] = token.stem

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1
        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)


def token_authors(request, token):
    date_filter = get_date_filter('start_date', 'end_date', request)
    analyses = models.Analysis.objects.filter(
        date_filter &
        get_algorithm_filter(request)
    )
    bow = Counter()
    for analysis in analyses:
        token_data = analysis.data[token]
        for author, author_data in token_data['authors'].items():
            bow.update({author: author_data['texts_count']})

    authors = data_models.Author.objects.all()
    final_dict = []
    for i, author in enumerate(bow.most_common(15)):
        author = authors.get(id=author[0])
        obj = {
            'token': author.name,
            'id': author.id,
        }

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1

        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)


def token_author_manifestations(request, token, author_id):
    date_filter = get_date_filter('speech__date', 'speech__date', request)
    token_filter = Q(token__stem=token) & date_filter
    token_filter = token_filter & Q(speech__author__id=author_id)
    man_tokens = models.SpeechToken.objects.filter(
        token_filter
    ).order_by('-occurrences')[:50]

    bow = Counter()
    for mt in man_tokens:
        bow.update({mt.speech: mt.occurrences})

    final_dict = []
    for i, speech in enumerate(bow.most_common()):
        speech = speech[0]
        obj = {
            'id': speech.id,
            'date': speech.date.strftime('%d/%m/%Y'),
            'time': speech.time.strftime('%H:%M'),
            'preview': speech.original[:70] + '...',
        }
        final_dict.append(obj)
    return JsonResponse(final_dict, safe=False)


def manifestation(request, speech_id, token):
    speech = get_object_or_404(Speech, pk=speech_id)
    original = re.sub(r'\b{}'.format(token),
                      '<span class="-highlight">{}</span>'.format(token),
                      speech.original)

    return JsonResponse(
        {
            'date': speech.date.strftime('%d/%m/%Y'),
            'time': speech.time.strftime('%H:%M'),
            'content': original,
        }
    )
