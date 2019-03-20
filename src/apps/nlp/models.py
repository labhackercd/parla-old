from django.db import models
import json


class Analysis(models.Model):
    TOKEN = 'token'
    AUTHOR = 'author'
    MANIFESTATION = 'manifestation'
    ANALYSIS_TYPE_CHOICES = (
        (TOKEN, 'Token'),
        (AUTHOR, 'Author'),
        (MANIFESTATION, 'Manifestation'),
    )

    MULTIGRAM_BOW_WITH_UNIGRAM = 'multigram_bow_with_unigram'
    MULTIGRAM_BOW_WITHOUT_UNIGRAM = 'multigram_bow_without_unigram'
    DECISION_TREE = 'decision_tree'
    ALGORITHM_CHOICES = (
        (MULTIGRAM_BOW_WITH_UNIGRAM, 'Multigrams Bag of Words with unigrams'),
        (MULTIGRAM_BOW_WITHOUT_UNIGRAM,
            'Multigrams Bag of Words without unigrams'),
        (DECISION_TREE, 'DecisionTree + Naive Bayes'),
    )

    analysis_type = models.CharField(max_length=20,
                                     choices=ANALYSIS_TYPE_CHOICES)
    algorithm = models.CharField(max_length=100, choices=ALGORITHM_CHOICES)
    phase = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    party = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
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
