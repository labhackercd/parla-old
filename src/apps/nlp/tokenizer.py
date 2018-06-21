from django.db import transaction
from apps.nlp import pre_processing, models as nlp
from apps.data import models


@transaction.atomic
def process_speech(speech, ngrams=1):
    speech.tokens.all().delete()
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


def process_speeches(ngrams=1):
    for speech in models.Speech.objects.filter(pre_processed=False):
        process_speech(speech, ngrams=ngrams)
