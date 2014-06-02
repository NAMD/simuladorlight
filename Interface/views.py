#coding:utf8
import json

from django.views.generic.base import TemplateView

from django.contrib import messages
import pandas as pd
from collections import OrderedDict
from Interface import Simulador

# Área de concessão da Light
municipios = [u'ITAGUAÍ', 'RIO DE JANEIRO', 'MESQUITA', u'SAO JOÃO DE MERITI', 'NOVA IGUAÇU', 'BELFORD ROXO',
              u'BARRA DO PIRAÍ',
              'VALENÇA', 'NILÓPOLIS', 'QUEIMADOS', 'VOLTA REDONDA', 'SEROPÉDICA', 'ENG PAULO DE FRONTIN',
              'DUQUE DE CAXIAS',
              'JAPERI', 'PATY DO ALFERES', 'SAPUCAIA', 'TRÊS RIOS', 'PIRAÍ', 'RIO CLARO', 'BARRA MANSA', 'PARACAMBI',
              'QUATIS',
              'MENDES', 'PINHEIRAL', 'MIGUEL PEREIRA', 'VASSOURAS', 'CARMO', 'PARAÍBA DO SUL', 'RIO DAS FLORES',
              'CDOR LEVY GASPARIAN',
]
geocodigos = [3302007, 3304557, 3302858, 3305109, 3303500, 3300456, 3300308, 3306107, 3303203, 3304144, 3306305,
              3305554,
              3301801, 3301702, 3302270, 3303856, 3305406, 3306008, 3304003, 3304409, 3300407, 3303609, 3304128,
              3302809, 3303955, 3302908,
              3306206, 3301207, 3303708, 3304524, 3300951,
]

mundict = OrderedDict(sorted(zip(municipios, geocodigos)))
geodict = OrderedDict(sorted(zip(geocodigos, municipios), key=lambda x: x[1]))

class HomePageView(TemplateView):
    template_name = 'mapaprocessos.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'Bem Vindo ao Simulador de Processos Judiciais.')
        horizonte = 60
        toi = 100
        corte = 100
        neg = 100
        try:
            toi = int(self.request.GET['toi'])
            corte = int(self.request.GET['corte'])
            neg = int(self.request.GET['neg'])
            horizonte = int(self.request.GET['horizonte'])
            processos = Simulador.simula(horizonte, toi, corte, neg)
        except KeyError:
            messages.error(self.request, "Todos os campos devem ser preenchidos")
            processos = Simulador.simula(horizonte, toi, corte, neg)
        processos = processos.set_index("geocodigo")
        context.update({"processos": processos.Novos.astype(int).to_json() if isinstance(processos,
                                                                             pd.DataFrame) else json.dumps({}),
                        'horizonte': horizonte,
                        'toi': toi,
                        'corte': corte,
                        'neg': neg,
                        'geodict': json.dumps(geodict),
                        'total': processos.Novos.astype(int).sum()

        })
        return context


class LocalAnalysisView(TemplateView):
    template_name = 'local.html'

    def get_context_data(self, **kwargs):
        context = super(LocalAnalysisView, self).get_context_data(**kwargs)
        municipio = int(self.request.GET.get("municipio", 3304557))

        horizonte = 60
        toi = 100
        corte = 100
        neg = 100
        try:
            toi = int(self.request.GET['toi'])
            corte = int(self.request.GET['corte'])
            neg = int(self.request.GET['neg'])
            horizonte = int(self.request.GET['horizonte'])
            processos = Simulador.simula_municipio(horizonte, toi, corte, neg, municipio)
        except KeyError:
            messages.error(self.request, "Todos os campos devem ser preenchidos")
            processos = Simulador.simula_municipio(horizonte, toi, corte, neg, municipio)
        #processos = processos.set_index("geocodigo")

        context.update({
            'municipio': geodict[municipio],
            'geocodigo': municipio,
            'mundict': json.dumps(list(mundict.items())),
            'geodict': json.dumps(geodict),
            'processos': int(processos),
            'horizonte': horizonte,
            'toi': toi,
            'corte': corte,
            'neg': neg,


        })
        return context

class SobreView(TemplateView):
    template_name = 'sobre.html'
    def get_context_data(self, **kwargs):
        context = super(SobreView, self).get_context_data(**kwargs)
        return context
