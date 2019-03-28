from django.db import transaction
from apps.data import models
from datetime import datetime
from html2text import HTML2Text
from functools import lru_cache
from urllib import parse
import click
import requests
import re


API_URL = 'http://vvmchjar01.redecamara.camara.gov.br:8082/fastsearchWS/' \
          'webservice/getConsulta'

DAY_ORDER = set([
    'DISCUSSÃO',
    'ENCAMINHAMENTO DE VOTAÇÃO',
    'ORIENTAÇÃO DE BANCADA',
    'COMO RELATOR',
    'PARECER',
    'COMO LÍDER',
    'PELA ORDEM',
    'DISCURSO ENCAMINHADO',
    'QUESTÃO DE ORDEM',
    'RECLAMAÇÃO',
    'FALA DO PRESIDENTE OU NO EXERCÍCIO DA PRESIDÊNCIA',
])

PHASE_RELATION = {
    'ABERTURA': 'OUTROS',
    'APARTE': 'OUTROS',
    'APRESENTAÇÃO DE PROPOSIÇÃO': 'OUTROS',
    'REPRESENTANTE DO PARTIDO': 'OUTROS',
    'OUTROS': 'OUTROS',
    'EXPLICAÇÃO PESSOAL': 'OUTROS',
    'DECLARAÇÃO DE VOTO': 'OUTROS',
    'ENCERRAMENTO': 'OUTROS',

    'COMUNICAÇÃO PARLAMENTAR': 'COMUNICAÇÕES PARLAMENTARES',
    'COMUNICAÇÕES PARLAMENTARES': 'COMUNICAÇÕES PARLAMENTARES',

    'BREVES COMUNICAÇÕES': 'BREVES COMUNICAÇÕES',
    'COMISSÃO GERAL': 'COMISSÃO GERAL',
    'GRANDE EXPEDIENTE': 'GRANDE EXPEDIENTE',
    'HOMENAGEM': 'HOMENAGEM',
    'PEQUENO EXPEDIENTE': 'PEQUENO EXPEDIENTE',

    'ORDEM DO DIA': 'ORDEM DO DIA',
    'REGISTRO DE VOTO': 'ORDEM DO DIA',
}

EXCLUDED_PHASES = set([
])


def get_url_params(initial_date, end_date, page):
    params = {
        'siglaAplicacao': 'novoDiscurso',
        'ordenacao': 'data',
        'ordenacaoDir': 'asc',
        'dataInicial': initial_date,
        'dataFinal': end_date,
        'pagina': page,
    }

    return params


def fetch_data(initial_date, end_date):
    response = requests.get(
        API_URL,
        params=get_url_params(initial_date, end_date, 1)
    )
    data = response.json()
    pages = data['qtdDePaginas']

    speeches_data = data['indexProfile']

    with click.progressbar(range(2, pages + 1),
                           label='Fetching speeches') as bar:
        for page in bar:
            response = requests.get(
                API_URL,
                params=get_url_params(initial_date, end_date, page)
            )
            data = response.json()
            speeches_data += data['indexProfile']

    return speeches_data


def fetch_author_photo(author):
    name = re.sub(r'\([^)]*\)', '', author.name)

    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
    today = datetime.now().date()
    params = {
        'nome': name.strip(),
        'dataInicio': '2015-01-01',
        'dataFim': today.strftime('%Y-%m-%d'),
        'ordem': 'DESC',
        'ordenarPor': 'idLegislatura'
    }
    response = requests.get(url, params=params, headers={
        'accept': 'application/json'
    })
    data = response.json()
    if len(data['dados']) > 0:
        author.photo_url = data['dados'][0]['urlFoto']
        author.save()
        return True
    else:
        return False


@lru_cache()
def create_author(name, party, state, gender, author_type):
    if name is None:
        name = ''
    else:
        name = re.sub(r'\([^)]*\)', '', name)

    if party is None:
        party = ''

    if state is None:
        state = ''

    if gender is None:
        gender = ''

    if author_type is None:
        author_type = ''

    return models.Author.objects.get_or_create(
        name=name.strip().title(),
        party=party.strip(),
        state=state.strip(),
        gender=gender.strip(),
        author_type=author_type.strip().title(),
    )[0]


def create_themes(themes):
    if themes is None:
        return []
    themes = themes.split(';')
    return [
        models.SpeechTheme.objects.get_or_create(name=theme)[0]
        for theme in themes
    ]


def create_speech(data, author):
    html2text = HTML2Text()
    html2text.ignore_links = True
    html2text.ignore_emphasis = True
    html2text.ignore_images = True
    html2text.ignore_tables = True

    html = data['companyteaser']
    regex = re.search('<body>(.*)</body>', html)
    if regex:
        html_body = regex.group(1)
    else:
        return None
    speech = re.sub('\n', ' ', html2text.handle(html_body)).strip()

    if data['keywords']:
        indexes = data['keywords'].strip()
    else:
        indexes = None

    if data['teaser']:
        summary = data['teaser'].strip()
    else:
        summary = None

    if data['fase']:
        original_phase = data['fase'].strip().upper()
    elif data['generic6']:
        original_phase = data['generic6']
    else:
        return None
    day_order_phase = None
    if original_phase in DAY_ORDER:
        original_phase = 'ORDEM DO DIA'
        day_order_phase = original_phase.strip().upper()

    phase = PHASE_RELATION[original_phase]

    if data['docdatetime'] is not None:
        speech_datetime = datetime.strptime(
            data['docdatetime'].strip(), '%Y-%m-%dT%H:%M:%SZ'
        )

    url_params = parse.parse_qs(data['url'])
    identifier = '{} {} {} {}'.format(
        url_params['numSessao'][0],
        url_params['numQuarto'][0],
        url_params['numOrador'][0],
        url_params['numInsercao'][0],
    )

    obj = models.Speech.objects.get_or_create(identifier=identifier, defaults={
        'content': speech,
        'html': html_body,
        'indexes': indexes,
        'date': speech_datetime.date(),
        'time': speech_datetime.time(),
        'phase': phase,
        'original_phase': original_phase,
        'day_order_phase': day_order_phase,
        'summary': summary,
        'author': author,
    })[0]

    return obj


@transaction.atomic
def create_speeches(speeches_data):
    with click.progressbar(speeches_data,
                           label='Saving speeches') as bar:
        for data in bar:
            if data['tiponorma'] == 'Plenário':
                author = create_author(
                    data['autor'],
                    data['partido'],
                    data['estado'],
                    data['emails'],
                    data['tipoautor']
                )
                fetch_author_photo(author)
                themes = create_themes(data['temas'])
                speech = create_speech(data, author)
                if speech:
                    speech.author = author
                    speech.save()

                    for theme in themes:
                        speech.themes.add(theme)
