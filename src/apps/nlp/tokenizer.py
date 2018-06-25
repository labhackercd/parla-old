from django.db import transaction
from apps.nlp import pre_processing, models as nlp
from apps.data import models


@transaction.atomic
def process_speech(speech, ngrams=1):
    speech.tokens.filter(token__ngrams=ngrams).delete()
    bow, reference = pre_processing.bow(speech.content, ngrams=ngrams)
    if len(bow) > 0:
        max_occurrences = max(bow.values())
        for stem, occurrences in bow.items():
            token = nlp.Token.objects.get_or_create(stem=stem)[0]
            token.ngrams = ngrams
            if ngrams == 1:
                for word, times in reference[stem].items():
                    token.add_original_word(word, times=times)
            else:
                words = [
                    reference[word].most_common(1)[0][0]
                    for word in stem.split(' ')
                ]
                token.add_original_word(' '.join(words))
            token.save()

            st = nlp.SpeechToken()
            st.speech = speech
            st.token = token
            st.occurrences = occurrences
            st.frequency = occurrences / max_occurrences
            st.save()
            print(st)

        speech.pre_processed = True
        speech.save()


def process_speeches(algorithm, ngrams=1):
    last = nlp.PreProcessing.objects.filter(algorithm=algorithm).last()
    if last:
        queryset = models.Speech.objects.filter(timestamp__gte=last.timestamp)
    else:
        queryset = models.Speech.objects.all()

    for speech in queryset:
        process_speech(speech, ngrams=ngrams)
    nlp.PreProcessing.objects.create(algorithm=algorithm)
