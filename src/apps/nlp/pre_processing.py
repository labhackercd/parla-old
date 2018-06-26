from collections import Counter
from functools import lru_cache
from nltk.corpus import floresta
from string import digits
import re
import nltk


def stemmize(token, stem_reference=None):
    token = token.casefold()
    stemmer = nltk.stem.RSLPStemmer()
    stemmed = stemmer.stem(token)

    if stem_reference is not None:
        reference = stem_reference.get(stemmed, Counter())
        reference.update([token])
        stem_reference[stemmed] = reference

    return stemmed


@lru_cache()
def simplify_tag(tag):
    if "+" in tag:
        return tag[tag.index("+") + 1:]
    else:
        return tag


@lru_cache()
def default_stopwords():
    twords = floresta.tagged_words()
    stopwords = nltk.corpus.stopwords.words('portuguese')
    stopwords += ['srs', 'sr', 'sras', 'sra', 'deputado', 'presidente',
                  'é', 'nº', 's.a.', 'v.exa.', 'v.exa', '#', 'anos', 'º',
                  'exa', 'mesa', 'legislatura', 'sessão', 'maioria']

    valid_tags = ['adj', 'n']
    for (word, tag) in twords:
        tag = simplify_tag(tag)
        words = word.casefold().split('_')
        if tag not in valid_tags:
            stopwords += words

    return list(set(stopwords))


@lru_cache()
def stemmize_stopwords():
    return list(set([
        stemmize(stopword)
        for stopword in default_stopwords()
    ]))


def remove_numeric_characters(text):
    remove_digits = str.maketrans('', '', digits)
    return text.translate(remove_digits)


def tokenize(text):
    return nltk.tokenize.word_tokenize(text, language='portuguese')


def clear_tokens(tokens, stopwords):
    stem_reference = {}
    cleared_tokens = [
        stemmize(token, stem_reference=stem_reference)
        for token in tokens
        if stemmize(token) not in stopwords
    ]
    return cleared_tokens, stem_reference


def clear_speech(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[OA] SRA?[\w\s.]+-', '', text)
    text = re.sub(r'PRONUNCIAMENTO[\sA-Z]+\s', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d', '', text)
    return text


@lru_cache()
def bow(text, method='frequency', ngrams=1):
    text = remove_numeric_characters(text)
    tokens = tokenize(text)
    stopwords = stemmize_stopwords()
    tokens, stem_reference = clear_tokens(tokenize(text), stopwords)

    text_bow = Counter([
        ' '.join(token)
        for token in nltk.ngrams(tokens, ngrams)
    ])
    return text_bow, stem_reference


def most_common_words(text, n=None):
    text_bow, reference = bow(text)
    most_common = []

    for token in text_bow.most_common(n):
        stem, frequency = token

        # reference[stem] is a Counter and most_comon(1) return a list
        # of tuples: ('word', occurrences)
        word = reference[stem].most_common(1)[0][0]
        most_common.append((word, frequency))
    return most_common
