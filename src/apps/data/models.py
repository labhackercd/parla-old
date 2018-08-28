from django.db import models


class Speech(models.Model):
    id_in_channel = models.CharField(max_length=50)
    content = models.TextField()
    indexes = models.TextField(null=True, blank=True)
    original = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('data.Author', on_delete=models.CASCADE,
                               related_name='speeches')

    class Meta:
        verbose_name = "Speech"
        verbose_name_plural = "Speeches"
        ordering = ['date', 'time']

    def __str__(self):
        return self.content[:50]


class Author(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name
