from django.core.management.base import BaseCommand
from apps.data import models
from calendar import monthrange
from dateutil.rrule import rrule, MONTHLY
from textblob import TextBlob
import csv
import datetime
import click

THEME_RELATION = {
    'Política, Partidos e Eleições': None,
    'Processo Legislativo e Atuação Parlamentar': None,
    'Homenagens e Datas Comemorativas': None,
    'Administração Pública': None,
    'Viação, Transporte e Mobilidade': 32,
    'Indústria, Comércio e Serviços': 23,
    'Defesa e Segurança': 9,
    'Agricultura, Pecuária, Pesca e Extrativismo': 2,
    'Trabalho e Emprego': 30,
    'Energia, Recursos Hídricos e Minerais': 18,
    'Ciência, Tecnologia e Inovação': 5,
    'Estrutura Fundiária': 20,
    'Economia': 16,
    'Meio Ambiente e Desenvolvimento Sustentável': 24,
    'Direito Penal e Processual Penal': 14,
    'Esporte e Lazer': 19,
    'Saúde': 29,
    'Educação': 17,
    'Direitos Humanos e Minorias': 15,
    'Direito e Defesa do Consumidor': 12,
    'Previdência e Assistência Social': 26,
    'Cidades e Desenvolvimento Urbano': 4,
    'Relações Internacionais e Comércio Exterior': 28,
    'Finanças Públicas e Orçamento': 21,
    'Direito e Justiça': 13,
    'Arte, Cultura e Religião': 3,
    'Turismo': 31,
    'Comunicações': 8,
    'Direito Civil e Processual Civil': 10,
    'Direito Constitucional': 11,
    'Ciências Sociais e Humanas': 7,
}


class Command(BaseCommand):
    help = 'Export train data'

    def handle(self, *args, **options):
        qs = models.Speech.objects.filter(author__author_type='Deputado')
        csv_file = open('train.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow([
            'sentencas',
            'nenhum',
            'adm-publica',
            'agricultura-pecuaria-pesca-extrativismo',
            'arte-cultura-religiao',
            'cidades-desenvolvimento-urbano',
            'ciencia-tecnologia-inovacao',
            'ciencias-exatas',
            'ciencias-sociais',
            'comunicacoes',
            'defesa-seguranca',
            'direito-civil',
            'direito-constitucional',
            'direito-consumidor',
            'direito-justica',
            'direito-penal',
            'direitos-humanos-minorias',
            'economia',
            'educacao',
            'energia-recursos-hidricos-minerais',
            'esporte-lazer',
            'estrutura-fundiaria',
            'financas-publicas-orcamento',
            'homenagens-datas-comemorativas',
            'industria-comercio-servicos',
            'meio-ambiente-desenvolvimento-sustentavel',
            'politica-partidos-eleicoes',
            'previdencia-assistencia-social',
            'processo-legislativo-atuacao-parlamentar',
            'relacoes-internacionais-comercio-exterior',
            'saude',
            'trabalho-emprego',
            'turismo',
            'viacao-transporte-mobilidade',
            'impeachment',
            'corrupção',
            'serviço-público',
            'reforma-política',
            'eleição',
        ])
        with click.progressbar(qs) as bar:
            for speech in bar:
                if speech.summary:
                    max_length = len(speech.content) * 1.1
                    min_length = len(speech.content) * 0.9
                    summary_len = len(speech.summary)
                    if summary_len > min_length and summary_len < max_length:
                        continue

                    themes = [''] * 38
                    for theme in speech.themes.all():
                        if THEME_RELATION[theme.name]:
                            themes[THEME_RELATION[theme.name]] = 'x'

                    if themes != [''] * 38:
                        blob = TextBlob(speech.summary)
                        for sentence in blob.sentences:
                            writer.writerow([sentence.raw] + themes)

        csv_file.close()
