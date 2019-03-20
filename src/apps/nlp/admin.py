from django.contrib import admin
from apps.nlp import models


@admin.register(models.Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'algorithm',
        'start_date',
        'end_date',
        'phase',
        'gender',
        'party',
        'state',
    )
    list_filter = (
        'algorithm',
        'phase',
        'gender',
        'party',
        'state',
    )
