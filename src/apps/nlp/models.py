from django.db import models
from collections import Counter
import json


class Token(models.Model):
    stem = models.CharField(max_length=255, unique=True)
    ngrams = models.IntegerField(default=1)
    _originals = models.TextField(default="{}")

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        ordering = ['stem']

    def __str__(self):
        return self.stem

    @property
    def original(self):
        originals = Counter(json.loads(self._originals))
        if len(originals) > 0:
            return originals.most_common(1)[0][0]
        else:
            return None

    def add_original_word(self, value, times=1):
        originals = Counter(json.loads(self._originals))
        originals.update({value: times})
        self._originals = json.dumps(originals)


class SpeechToken(models.Model):
    speech = models.ForeignKey('data.Speech', related_name='tokens',
                               on_delete=models.CASCADE)
    token = models.ForeignKey('nlp.Token', related_name='speeches',
                              on_delete=models.CASCADE)
    use_indexes = models.BooleanField(default=False)
    occurrences = models.IntegerField(default=0)
    frequency = models.FloatField(default=0)

    class Meta:
        verbose_name = "Speech Token"
        verbose_name_plural = "Speech Tokens"
        ordering = ['occurrences']

    def __str__(self):
        return '{} in {}'.format(self.token.stem, self.speech.__str__())


class PreProcessing(models.Model):
    algorithm = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PreProcessing"
        verbose_name_plural = "PreProcessings"
        ordering = ['timestamp']

    def __str__(self):
        return '{} at {}'.format(self.algorithm, self.timestamp)


class Analysis(models.Model):
    TOKEN = 'token'
    AUTHOR = 'author'
    MANIFESTATION = 'manifestation'
    ANALYSIS_TYPE_CHOICES = (
        (TOKEN, 'Token'),
        (AUTHOR, 'Author'),
        (MANIFESTATION, 'Manifestation'),
    )

    UNIGRAM_BOW = 'unigram_bow'
    BIGRAM_BOW = 'bigram_bow'
    ALGORITHM_CHOICES = (
        (UNIGRAM_BOW, 'Unigram Bag of Words'),
        (BIGRAM_BOW, 'Bigram Bag of Words'),
    )

    analysis_type = models.CharField(max_length=20,
                                     choices=ANALYSIS_TYPE_CHOICES)
    algorithm = models.CharField(max_length=100, choices=ALGORITHM_CHOICES)
    use_indexes = models.BooleanField(default=False)
    stem = models.CharField(max_length=255, null=True, blank=True)
    author_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    _data = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Analysis"
        verbose_name_plural = "Analyses"

    def __str__(self):
        return '{}: {} - {}'.format(self.analysis_type, self.start_date,
                                    self.end_date)

    @property
    def data(self):
        if self._data:
            return json.loads(self._data)
        else:
            return {}

    @data.setter
    def data(self, value):
        self._data = json.dumps(value)
