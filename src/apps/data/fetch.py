from django.conf import settings
from django.db import transaction
from apps.data import models
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
    url = '{}{}/?{}'.format(
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


def create_speeches(data_list):
    speech_list = []
    for data in data_list:
        speech = models.Speech()
        speech.id_in_channel = data['id_in_channel']
        speech.content = data['content']
        speech.author = data['profile']['author']['name']
        timestamp = datetime.strptime(data['timestamp'][:-6],
                                      '%Y-%m-%dT%H:%M:%S')
        speech.date = timestamp.date()
        speech.time = timestamp.time()
        for attr in data['attrs']:
            if hasattr(speech, attr['field']):
                setattr(speech, attr['field'], attr['value'])

        speech_list.append(speech)
    return speech_list


def save(model_list):
    with transaction.atomic():
        for model_instance in model_list:
            model_instance.save()
