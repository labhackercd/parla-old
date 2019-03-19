from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier
from textblob import TextBlob
from collections import Counter
from functools import lru_cache
from nltk.corpus import floresta
from string import punctuation
from django.conf import settings
from apps.nlp import stopwords
from apps.nlp import cache
import pickle
import nltk
import csv
import re
import os


LABELS_RELATION = {
    0: 'none',
    1: 'adm-publica',
    2: 'agricultura-pecuaria-pesca-extrativismo',
    3: 'arte-cultura-religiao',
    4: 'cidades-desenvolvimento-urbano',
    5: 'ciencia-tecnologia-inovacao',
    6: 'ciencias-exatas',
    7: 'ciencias-sociais',
    8: 'comunicacoes',
    9: 'defesa-seguranca',
    10: 'direito-civil',
    11: 'direito-constitucional',
    12: 'direito-consumidor',
    13: 'direito-justica',
    14: 'direito-penal',
    15: 'direitos-humanos-minorias',
    16: 'economia',
    17: 'educacao',
    18: 'energia-recursos-hidricos-minerais',
    19: 'esporte-lazer',
    20: 'estrutura-fundiaria',
    21: 'financas-publicas-orcamento',
    22: 'homenagens-datas-comemorativas',
    23: 'industria-comercio-servicos',
    24: 'meio-ambiente-desenvolvimento-sustentavel',
    25: 'politica-partidos-eleicoes',
    26: 'previdencia-assistencia-social',
    27: 'processo-legislativo-atuacao-parlamentar',
    28: 'relacoes-internacionais-comercio-exterior',
    29: 'saude',
    30: 'trabalho-emprego',
    31: 'turismo',
    32: 'viacao-transporte-mobilidade',
    33: 'impeachment',
    34: 'corrupcao',
    35: 'servico-publico',
    36: 'reforma-politica',
    37: 'eleicao',
}

EXCLUDED_THEMES = [1, 22, 25, 27, 6, 7]

MACRO_THEMES_RELATION = {
    'cidades-desenvolvimento-urbano': 'cidades-transportes',
    'viacao-transporte-mobilidade': 'cidades-transportes',

    'comunicacoes': 'ct-comunicacoes',
    'ciencia-tecnologia-inovacao': 'ct-comunicacoes',
    'ciencias-exatas': 'ct-comunicacoes',

    'defesa-seguranca': 'seguranca',

    'previdencia-assistencia-social': 'trabalho-previdencia-assistencia',
    'trabalho-emprego': 'trabalho-previdencia-assistencia',

    'relacoes-internacionais-comercio-exterior': 'relacoes-exteriores',

    'saude': 'saude',

    'arte-cultura-religiao': 'educacao-cultura-esporte',
    'educacao': 'educacao-cultura-esporte',
    'esporte-lazer': 'educacao-cultura-esporte',
    'turismo': 'educacao-cultura-esporte',

#     'homenagens-datas-comemorativas': 'politica-adm-publica',
#     'politica-partidos-eleicoes': 'politica-adm-publica',
#     'processo-legislativo-atuacao-parlamentar': 'politica-adm-publica',
#     'adm-publica': 'politica-adm-publica',

    'ciencias-sociais': 'direitos-humanos',
    'direitos-humanos-minorias': 'direitos-humanos',

    'agricultura-pecuaria-pesca-extrativismo': 'agropecuaria',
    'estrutura-fundiaria': 'agropecuaria',

    'financas-publicas-orcamento': 'economia',
    'economia': 'economia',

    'meio-ambiente-desenvolvimento-sustentavel': 'meio-ambiente-energia',
    'energia-recursos-hidricos-minerais': 'meio-ambiente-energia',

    'direito-consumidor': 'consumidor',
    'industria-comercio-servicos': 'consumidor',

    'direito-civil': 'justica',
    'direito-constitucional': 'justica',
    'direito-justica': 'justica',
    'direito-penal': 'justica',

    'impeachment': 'adm-publica',
    'corrupcao': 'adm-publica',
    'servico-publico': 'adm-publica',

    'reforma-politica': 'politica-partidos-eleicoes',
    'eleicao': 'politica-partidos-eleicoes',
}


def clear_speech(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[OA] SRA?[\w\s.]+-', '', text)
    text = re.sub(r'PRONUNCIAMENTO[\sA-Z]+\s', '', text)
    text = re.sub(r'\s[\.\"]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[Vv]\.[Ee][Xx][Aa]\.', 'v.exa', text)
    text = re.sub(r'[Aa][Rr][Tt]\.', 'art', text)
    text = re.sub(r'[Ss][Rr][Ss]?\.', 'sr', text)
    text = re.sub(r'[Ss][Rr][Aa][Ss]?\.', 'sr', text)
    text = re.sub(r'\d', '', text)
    return text.strip()


@lru_cache()
def simplify_tag(tag):
    if '+' in tag:
        return tag[tag.index("+") + 1:]
    else:
        return tag


stemmer = nltk.RSLPStemmer()


@lru_cache()
def stem_stopwords():
    floresta_twords = floresta.tagged_words()
    stem_stopwords = stopwords.EXTRA_STOPWORDS + [x for x in punctuation]
    stem_stopwords = [stemmer.stem(word) for word in stem_stopwords]
    for (word, tag) in floresta_twords:
        tag = simplify_tag(tag)
        words = word.casefold().split('_')
        if tag not in ('adj', 'n', 'prop', 'nprop', 'est', 'npro'):
            stem_stopwords += [stemmer.stem(word) for word in words]

    return list(set(stem_stopwords))


def freq_feature_extractor(document):
    regex = re.compile('[%s]' % re.escape(punctuation))
    document = regex.sub(' ', document.casefold())
    tokens = nltk.tokenize.word_tokenize(document)
    tokens = [
        stemmer.stem(token)
        for token in tokens
        if stemmer.stem(token) not in stem_stopwords()
    ]
    dist = nltk.FreqDist(tokens)

    features = {
        stem: True
        for stem, _ in dist.most_common()
    }
    return features


@lru_cache()
def load_dataset():
    content_dataset = []
    theme_dataset = []
    trainset_dir = os.path.join(settings.BASE_DIR, 'apps/nlp')
    with open(os.path.join(trainset_dir, 'theme-dataset.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            for idx, category in enumerate(row[1:-1]):
                if category != '' and idx > 0 and idx not in EXCLUDED_THEMES:
                    theme_dataset.append((row[0], LABELS_RELATION[idx]))
                    content_dataset.append((row[0], 'content'))
                elif category != '' and idx == 0:
                    content_dataset.append((row[0], 'useless'))
    return content_dataset, theme_dataset


@lru_cache()
def get_content_classifier():
    content_dataset, _ = load_dataset()
    pkl_file = os.path.join(settings.BASE_DIR,
                            'apps/nlp/content_classifier.pkl')
    try:
        classifier = pickle.load(open(pkl_file, 'rb'))
    except FileNotFoundError:
        classifier = NaiveBayesClassifier(
            content_dataset,
            feature_extractor=freq_feature_extractor
        )
        classifier.train()
        pickle.dump(classifier, open(pkl_file, 'wb'))
    return classifier


@lru_cache()
def get_theme_classifier():
    _, dataset = load_dataset()
    pkl_file = os.path.join(settings.BASE_DIR,
                            'apps/nlp/theme_classifier.pkl')
    try:
        classifier = pickle.load(open(pkl_file, 'rb'))
    except FileNotFoundError:
        classifier = DecisionTreeClassifier(
            dataset,
            feature_extractor=freq_feature_extractor
        )
        classifier.train()
        pickle.dump(classifier, open(pkl_file, 'wb'))
    return classifier


def has_content(sentence):
    content_classifier = get_content_classifier()

    prob_dist = content_classifier.prob_classify(sentence)
    if prob_dist.prob(prob_dist.max()) > 0.8:
        if prob_dist.max() == 'content':
            return True
        else:
            return False
    else:
        return False


def classify_sentence(sentence):
    if has_content(sentence):
        theme_classifier = get_theme_classifier()
        return theme_classifier.classify(sentence)
    else:
        return None


def classify_speech(speech, normalize=True):
    cleaned_text = clear_speech(speech)
    blob = TextBlob(cleaned_text)
    classes = [classify_sentence(sentence.raw) for sentence in blob.sentences]
    classes = list(filter(None, classes))
    speech_themes = Counter(classes)

    if normalize:
        # Normalize speech_themes
        total = 1.0 * len(classes)
        for theme in speech_themes:
            speech_themes[theme] /= total

    return speech_themes
