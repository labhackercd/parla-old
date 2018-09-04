from django.conf import settings
from unidecode import unidecode
from textblob.classifiers import NaiveBayesClassifier as Classifier
from apps.nlp import cache
import json
import os


def normalize(text):
    return unidecode(text.lower().strip('.,:?!- '))


def get_initial_trainset():
    trainset_dir = os.path.join(settings.BASE_DIR, 'apps/nlp')
    with open(os.path.join(trainset_dir, 'thesaurus.json')) as thes:
        thesaurus = json.load(thes)
        trainset = [
            (normalize(token), theme)
            for theme, tokens in thesaurus.items()
            for token in tokens
        ]
    return trainset


def classifier():
    def get_classifier():
        return Classifier(get_initial_trainset())
    return cache.load_from_cache('theme_classifier', get_classifier)
