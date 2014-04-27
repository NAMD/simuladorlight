from django.shortcuts import render
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

        try:
            toi = int(self.request.GET['toi'])
            corte = int(self.request.GET['corte'])
            neg = int(self.request.GET['neg'])
            horizonte = int(self.request.GET['horizonte'])
            processos = Simulador.simula(horizonte, toi, corte, neg)
        except KeyError:
            messages.error(self.request, "Todos os campos devem ser preenchidos")
            processos = json.dumps({})
        processos = processos.set_index("geocodigo")
        context.update({"processos": processos.Novos.to_json() if isinstance(processos, pd.DataFrame) else json.dumps({})

        })
        return context
