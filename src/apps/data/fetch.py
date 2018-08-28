from django.conf import settings
from django.db import transaction
from apps.data import models
from apps.nlp import pre_processing
from datetime import datetime
import requests
import urllib


def url_parameters(resource_id, page):
    params = {
        'manifestation_type__id': resource_id,
        'page': page,
    }

    last_speech = models.Speech.objects.last()
    if last_speech:
        params['timestamp__gte'] = last_speech.date.strftime('%Y-%m-%d')

    return urllib.parse.urlencode(params)


def get_json_data(resource_name, resource_id, page=1):
    url = '{}{}?{}'.format(
        settings.BABEL_API_URL,
        resource_name,
        url_parameters(resource_id, page)
    )

    full_data = []

    response = requests.get(url)
    data = response.json()
    full_data.extend(data['results'])
    if data['next']:
        full_data.extend(
            get_json_data(resource_name, resource_id, page + 1)
        )

    return full_data


@transaction.atomic
def create_author(profile_url):
    response = requests.get(profile_url)
    author_data = response.json()
    try:
        author = models.Author.objects.get(id=author_data['id'])
    except models.Author.DoesNotExist:
        author = models.Author()
        author.id = author_data['id']
    author.name = author_data['id_in_channel']
    author.save()
    return author


@transaction.atomic
def create_speeches(data_list):
    speech_list = []
    for data in data_list:
        try:
            speech = models.Speech.objects.get(id=data['id'])
        except models.Speech.DoesNotExist:
            speech = models.Speech()
            speech.id = data['id']
        speech.id_in_channel = data['id_in_channel']
        speech.author = create_author(data['profile'])
        timestamp = datetime.strptime(data['timestamp'][:-6],
                                      '%Y-%m-%dT%H:%M:%S')
        speech.date = timestamp.date()
        speech.time = timestamp.time()
        for attr in data['attrs']:
            if hasattr(speech, attr['field']):
                setattr(speech, attr['field'], attr['value'])
            if attr['field'] == 'indexacao':
                speech.indexes = attr['value']

        speech.content = pre_processing.clear_speech(speech.original)
        speech.save()
        print(speech)
        speech_list.append(speech)
    return speech_list
