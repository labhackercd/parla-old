from django.views.generic import TemplateView
from apps.data import models
from apps.nlp import analysis


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = models.Speech.objects.all()

        context['states'] = analysis.get_states(qs)
        context['phases'] = analysis.get_phases(qs)
        context['parties'] = analysis.get_parties(qs)
        context['genders'] = ['M', 'F']

        return context
