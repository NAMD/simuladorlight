from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.contrib import messages
import pandas as pd
import json
from Interface import Simulador



class HomePageView(TemplateView):
    template_name = 'mapaprocessos.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Bem Vindo ao Simulador de Processos Judiciais.')
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
        context.update({"processos": processos.Novos.to_json() if isinstance(processos,
                                                                             pd.DataFrame) else json.dumps({}),
                        'horizonte': horizonte,
                        'toi': toi,
                        'corte': corte,
                        'neg': neg,

        })
        return context

class LocalAnalysisView(TemplateView):
    template_name = 'local.html'

    def get_context_data(self, **kwargs):
        context = super(LocalAnalysisView)

        context.update({

        })
        return context
