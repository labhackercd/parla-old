from django.db import models
from django_pandas.managers import DataFrameManager


class Speech(models.Model):
    identifier = models.CharField(max_length=50)
    content = models.TextField()
    html = models.TextField()
    indexes = models.TextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    phase = models.CharField(max_length=50)
    original_phase = models.CharField(max_length=50)
    day_order_phase = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    tokens = models.TextField(null=True, blank=True)
    themes = models.ManyToManyField('data.SpeechTheme',
                                    related_name='speeches',
                                    blank=True)
    author = models.ForeignKey('data.Author', on_delete=models.CASCADE,
                               related_name='speeches')

    objects = DataFrameManager()

    class Meta:
        verbose_name = "Speech"
        verbose_name_plural = "Speeches"
        ordering = ['date', 'time']

    def __str__(self):
        return self.content[:50]


class SpeechTheme(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Speech Theme"
        verbose_name_plural = "Speech Themes"

    def __str__(self):
        return self.name


class StemToken(models.Model):
    stem = models.CharField(primary_key=True, max_length=50)
    original = models.CharField(max_length=250)


class Author(models.Model):
    name = models.CharField(max_length=250)
    party = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=250, null=True, blank=True)
    author_type = models.CharField(max_length=250, null=True, blank=True)
    photo_url = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name
