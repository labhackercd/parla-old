from django.db import models


class Speech(models.Model):
    id_in_channel = models.CharField(max_length=50)
    content = models.TextField()
    original = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    author = models.CharField(max_length=255)
    pre_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Speech"
        verbose_name_plural = "Speeches"
        ordering = ['date', 'time']

    def __str__(self):
        return self.content[:50]
