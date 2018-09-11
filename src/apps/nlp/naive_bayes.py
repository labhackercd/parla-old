from django.conf import settings
from unidecode import unidecode
from textblob.classifiers import NaiveBayesClassifier as Classifier
from apps.nlp.pre_processing import bow
from apps.nlp import cache
import json
import os


def normalize(text):
    return unidecode(text.lower().strip('.,:?!- '))


def get_initial_trainset():
    trainset_dir = os.path.join(settings.BASE_DIR, 'apps/nlp')
    with open(os.path.join(trainset_dir, 'thesaurus.json')) as thes:
        thesaurus = json.load(thes)
        del thesaurus['politica']
        del thesaurus['gestao']
        del thesaurus['desenvolvimento-regional']
        del thesaurus['comunicacao-social']
        del thesaurus['adm-publica']
        trainset = [
            (normalize(token), theme)
            for theme, tokens in thesaurus.items()
            for token in tokens
        ]
    return trainset


def extract(text):
    text_bow, _ = bow(text)
    return dict(text_bow)


def get_classifier():
    return Classifier(get_initial_trainset(), feature_extractor=extract)


def classifier():
    return cache.load_from_cache('theme_classifier', get_classifier)
