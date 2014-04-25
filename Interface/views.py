from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.contrib import messages

import json



class HomePageView(TemplateView):
    template_name = 'mapaprocessos.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Bem Vindo ao Simulador de Processos Judiciais.')

        context.update({

        })
        return context
