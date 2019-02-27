from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.nlp import models
from apps.data import models as data_models
from apps.data.models import Speech
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from collections import Counter
from django.http import JsonResponse
import re
from django.utils.text import slugify


def get_date_filter(request):
    date_filter = Q()
    final = date.today()
    init = final.replace(day=1)
    initial_date = request.GET.get('initial_date', str(init))
    final_date = request.GET.get('final_date', str(final))

    if initial_date:
        initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        date_filter = date_filter & Q(start_date__gte=initial_date)

    if final_date:
        final_date = datetime.strptime(final_date, '%Y-%m-%d')
        date_filter = date_filter & Q(end_date__lte=final_date)

    return date_filter


def get_algorithm_filter(request):
    algorithm = request.GET.get('algorithm', None)
    if algorithm:
        return Q(algorithm=algorithm)
    else:
        return Q(algorithm='multigram_bow_without_unigram')


LABELS_RELATION = {
    'adm-publica': 'Administração Pública',
    'agricultura-pecuaria-pesca-extrativismo': 'Agricultura, Pecuária, '
                                               'Pesca e Extrativismo',
    'arte-cultura-religiao': 'Arte, Cultura e Religião',
    'cidades-desenvolvimento-urbano': 'Cidades e Desenvolvimento Urbano',
    'ciencia-tecnologia-inovacao': 'Ciência, Tecnologia e Inovação',
    'ciencias-exatas': 'Ciências Exatas',
    'ciencias-sociais': 'Ciências Sociais',
    'comunicacoes': 'Comunicações',
    'defesa-seguranca': 'Defesa e Segurança',
    'direito-civil': 'Direito Civil e Processual Civil',
    'direito-constitucional': 'Direito Constitucional',
    'direito-consumidor': 'Direito e Defesa do Consumidor',
    'direito-justica': 'Direito e Justiça',
    'direito-penal': 'Direito Penal e Processual Penal',
    'direitos-humanos-minorias': 'Direitos Humanos e Minorias',
    'economia': 'Economia',
    'educacao': 'Educação',
    'energia-recursos-hidricos-minerais': 'Energia, Recursos Hídricos '
                                          'e Minerais',
    'esporte-lazer': 'Esporte e Lazer',
    'estrutura-fundiaria': 'Estrutura Fundiária',
    'financas-publicas-orcamento': 'Finanças Públicas e Orçamento',
    'homenagens-datas-comemorativas': 'Homenagens e Datas Comemorativas',
    'industria-comercio-servicos': 'Indústria, Comércio e Serviços',
    'meio-ambiente-desenvolvimento-sustentavel': 'Meio Ambiente e '
                                                 'Desenvolvimento Sustentável',
    'politica-partidos-eleicoes': 'Política, Partidos e Eleições',
    'previdencia-assistencia-social': 'Previdência e Assistência Social',
    'processo-legislativo-atuacao-parlamentar': 'Processo Legislativo e '
                                                'Atuação Parlamentar',
    'relacoes-internacionais-comercio-exterior': 'Relações Internacionais e '
                                                 'Comércio Exterior',
    'saude': 'Saúde',
    'trabalho-emprego': 'Trabalho e Emprego',
    'turismo': 'Turismo',
    'viacao-transporte-mobilidade': 'Viação, Transporte e Mobilidade',
}


def tokens(request):
    algorithm = request.GET.get('algorithm', 'multigram_bow_without_unigram')
    date_filter = get_date_filter(request)
    analyses = models.Analysis.objects.filter(
        date_filter &
        get_algorithm_filter(request)
    )

    bow = Counter()
    for analysis in analyses:
        for stem, token_data in analysis.data.items():
            bow.update({stem: token_data['authors_count']})

    final_dict = []
    for i, stem in enumerate(bow.most_common(20)):
        obj = {}
        if algorithm == 'decision_tree':
            obj['id'] = stem[0]
            obj['token'] = LABELS_RELATION[stem[0]]
            obj['stem'] = stem[0]
        elif (algorithm == 'multigram_bow_with_unigram' or
              algorithm == 'multigram_bow_without_unigram'):
            obj['id'] = slugify(stem[0])
            obj['token'] = stem[0]
            obj['stem'] = stem[0]
        else:
            obj['id'] = stem[0]
            obj['token'] = stem[0]
            obj['stem'] = stem[0]

        if i > 0:
            previous = final_dict[i - 1]
            obj['size'] = previous['size'] * 0.7
        else:
            obj['size'] = 1
        final_dict.append(obj)

    return JsonResponse(final_dict, safe=False)


def token_authors(request, token):
    date_filter = get_date_filter(request)
    analyses = models.Analysis.objects.filter(
        date_filter &
        get_algorithm_filter(request)
    )
    bow = Counter()
    for analysis in analyses:
        token_data = analysis.data.get(token, None)
        if token_data:
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
    date_filter = get_date_filter(request)
    analyses = models.Analysis.objects.filter(
        date_filter &
        get_algorithm_filter(request)
    )
    bow = Counter()
    for analysis in analyses:
        token_data = analysis.data.get(token, None)
        if token_data:
            author_data = token_data['authors'].get(str(author_id), None)
            if author_data:
                for speech in author_data['texts']:
                    bow.update(speech)

    final_dict = []
    max_occurrence = bow.most_common(1)[0][1]
    for speech_id, occurrences in bow.most_common(50):
        speech = data_models.Speech.objects.get(pk=speech_id)
        obj = {
            'id': speech.id,
            'date': speech.date.strftime('%d/%m/%Y'),
            'time': speech.time.strftime('%H:%M'),
            'preview': speech.content[:70] + '...',
            'ratio': occurrences / max_occurrence,
        }
        final_dict.append(obj)
    return JsonResponse(final_dict, safe=False)


def manifestation(request, speech_id, token):
    speech = get_object_or_404(Speech, pk=speech_id)
    search = re.compile(r'\b(%s)\b' % token, re.I)
    original = search.sub('<span class="-highlight">\\1</span>',
                          speech.original)

    return JsonResponse(
        {
            'date': speech.date.strftime('%d/%m/%Y'),
            'time': speech.time.strftime('%H:%M'),
            'content': original,
            'indexes': speech.indexes,
        }
    )


def dateRange(request):
    try:
        bound_min = Speech.objects.first().date.strftime('%Y-%m')
    except Speech.DoesNotExist:
        bound_min = ''
    bound_max = date.today() + relativedelta(months=1)
    bound_max = bound_max.strftime('%Y-%m')
    today = date.today()
    min_date = date(today.year, 1, 1)
    default_min = min_date.strftime('%Y-%m')
    default_max = today.strftime('%Y-%m')

    return JsonResponse(
        {
            'bound_min': bound_min,
            'bound_max': bound_max,
            'default_min': default_min,
            'default_max': default_max,
        }
    )
