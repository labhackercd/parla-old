from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from apps.data import models, fetch


@admin.register(models.Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = (
        'identifier',
        'date',
        'time',
        'summary',
    )
    list_filter = (
        'date',
        'phase',
        'themes',
        'author__author_type',
    )
    search_fields = (
        'content',
        'author__name'
    )


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'party',
        'state',
        'gender',
        'author_type',
    )
    list_filter = (
        'gender',
        'author_type',
        'state',
        'party',
    )
    actions = ['fetch_photo']

    def fetch_photo(self, request, queryset):
        success = 0
        for author in queryset:
            if fetch.fetch_author_photo(author):
                success += 1
            else:
                self.message_user(
                    request,
                    _('Author "{}" not found on Câmara dos Deputados '
                      'API.'.format(author.name)), level='error')
        if success > 0:
            self.message_user(
                request,
                _('{} author(s) photo was fetched '
                  'successfully.'.format(success)))
