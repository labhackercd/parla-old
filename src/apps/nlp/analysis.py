from django.db.models import Q
from django.db import transaction
from dateutil.rrule import rrule, MONTHLY
from collections import Counter
from calendar import monthrange
from click import progressbar, secho
import datetime

from apps.nlp import models as nlp
from apps.data import models as data


def date_filter(start_date, end_date):
    return Q(speech__date__gte=start_date, speech__date__lte=end_date)


def months(queryset):
    start_date = queryset.first().speech.date
    end_date = queryset.last().speech.date
    return rrule(MONTHLY, dtstart=start_date, until=end_date)


@transaction.atomic()
def ngrams_token_analysis(ngrams=1):
    speech_tokens = nlp.SpeechToken.objects.filter(
        token__ngrams=ngrams
    ).order_by('speech__date')

    if ngrams == 1:
        algorithm = nlp.Analysis.UNIGRAM_BOW
    else:
        algorithm = nlp.Analysis.BIGRAM_BOW

    for date in months(speech_tokens):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)

        secho('Fetching data from {} to {}'.format(start_date, end_date))
        queryset = speech_tokens.filter(date_filter(start_date, end_date))

        bow = Counter()
        secho('Processing speeches')
        with progressbar(queryset) as bar:
            for speech_token in bar:
                bow.update({speech_token.token.stem: speech_token.occurrences})

        if len(bow) > 0:
            secho('\nSaving analysis')
            analysis = nlp.Analysis.objects.get_or_create(
                start_date=start_date,
                end_date=end_date,
                algorithm=algorithm,
                analysis_type=nlp.Analysis.TOKEN
            )[0]
            analysis.data = bow
            analysis.save()
        secho('Done!')


@transaction.atomic()
def ngrams_author_analysis(ngrams=1):
    tokens = nlp.Token.objects.filter(ngrams=ngrams)
    speech_tokens = nlp.SpeechToken.objects.filter(
        token__ngrams=ngrams
    ).order_by('speech__date')

    if ngrams == 1:
        algorithm = nlp.Analysis.UNIGRAM_BOW
    else:
        algorithm = nlp.Analysis.BIGRAM_BOW

    for date in months(speech_tokens):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        with progressbar(tokens) as bar:
            for token in bar:
                queryset = speech_tokens.filter(
                    date_filter(start_date, end_date) &
                    Q(token__stem=token.stem)
                )

                bow = Counter()
                for st in queryset:
                    bow.update(
                        {st.speech.author.id: st.occurrences}
                    )

                if len(bow):
                    analysis = nlp.Analysis.objects.get_or_create(
                        start_date=start_date,
                        end_date=end_date,
                        algorithm=algorithm,
                        stem=token.stem,
                        analysis_type=nlp.Analysis.AUTHOR
                    )[0]
                    analysis.data = bow
                    analysis.save()


@transaction.atomic()
def ngrams_speech_analysis(ngrams=1):
    authors = data.Author.objects.all()
    tokens = nlp.Token.objects.filter(ngrams=ngrams)
    speech_tokens = nlp.SpeechToken.objects.filter(
        token__ngrams=ngrams
    ).order_by('speech__date')

    if ngrams == 1:
        algorithm = nlp.Analysis.UNIGRAM_BOW
    else:
        algorithm = nlp.Analysis.BIGRAM_BOW

    for date in months(speech_tokens):
        days = monthrange(date.year, date.month)[1]
        start_date = datetime.datetime(date.year, date.month, 1)
        end_date = datetime.datetime(date.year, date.month, days)
        secho('Fetching data from {} to {}'.format(start_date, end_date))

        with progressbar(authors) as bar:
            for author in bar:
                for token in tokens:
                    queryset = speech_tokens.filter(
                        date_filter(start_date, end_date) &
                        Q(token__stem=token.stem)
                    )
                    bow = Counter()
                    for st in queryset:
                        bow.update({st.speech.id: st.occurrences})

                    if len(bow) > 0:
                        analysis = nlp.Analysis.objects.get_or_create(
                            start_date=start_date,
                            end_date=end_date,
                            algorithm=algorithm,
                            stem=token.stem,
                            author_id=author.id,
                            analysis_type=nlp.Analysis.MANIFESTATION
                        )[0]
                        analysis.data = bow
                        analysis.save()
