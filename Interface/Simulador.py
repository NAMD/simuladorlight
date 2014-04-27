#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd



def carrega_dados():
    """
    Lê os dados brutos.
    :rtype : pd.DataFrame
    """
    df = pd.read_csv('tabelaparaosimulador.csv.gz',
                     names=["municipio", "contrato", "dt_inicio", "dt_fim", "data_processo", "data_corte",
                            "data_toi", "data_reclamacao", "data_negativacao"],
                     index_col=0, parse_dates=True, compression='gzip'
    )
    return df


def calcula_prevalencias(dados):
    """
    Calcula distribuições de probabilidades de notas por município
    :rtype : tuple
    :param dados: Dataframe com os dados produzida por `carrega_dados`
    """
    for n in dados.columns:
        if n.startswith("data_") or n == "contrato":
            dados[n] = pd.notnull(dados[n])
            dados[n].astype(int)

    del dados['dt_inicio'], dados['dt_fim']
    totais = dados.groupby(level=0).sum()
    totais["sem_nota"] = totais.contrato - (totais.data_corte + totais.data_toi + totais.data_negativacao + totais.data_reclamacao)
    municipios = totais.index.tolist()
    prevalencias = pd.DataFrame(index=municipios)
    for n in totais.columns:
        if n == "contrato":
            prevalencias[n] = totais[n] / totais[n].sum()
        else:
            prevalencias[n.split('_')[1]] = totais[n] / totais[n].sum()

            #print (prevalencias[:10])
    return prevalencias, totais


def carrega_parametros():
    """
    Lê os parâmetros da análise de sobrevivência, e retorna um dataframe indexado por município.
    :rtype : pd.DataFrame
    """
    parametros = pd.read_csv("alphas.csv", index_col=1, header=0)
    #print(parametros[:10])
    return parametros


def distribui_notas(ncorte, nneg, ntoi, processos):
    """
    Distribui Notas de acordo com suas prevalências
    :param ncorte: Numero total de notas de corte
    :param nneg: Numero total de notas de negativação
    :param ntoi: Numero total de notas de toi
    :param processos: DataFrame com indice de municípios e seus geocódigos
    :return: Dataframe com as notas distribuídas
    """
    processos["tois_apl"] = ntoi * PREVALENCIAS.toi
    processos["cortes_apl"] = ncorte * PREVALENCIAS.corte
    processos["negs_apl"] = nneg * PREVALENCIAS.negativacao
    return processos


def simula(horizonte=30, ntoi=0, ncorte=0, nneg=0):
    """
    Esta função calcula o número esperado de processos judiciais com base no estado atual do sistema e o número de
    notas a serem aplicadas
    :param horizonte: Horizonte de previsão em dias
    :param ntoi: Numero de novos tois a serem aplicados
    :param ncorte: Numero de novos cortes a serem aplicados
    :param nneg: Número de negativações a serem aplicados
    """
    processos = pd.DataFrame(index=PARAMETROS.index.tolist())
    processos['geocodigo'] = PARAMETROS.geocodigo
    total_notas = ntoi + ncorte + nneg
    # Distribuindo as notas por municipio de acordo com as prevalencias
    processos = distribui_notas(ncorte, nneg, ntoi, processos)
    processos['notas_total'] = processos.tois_apl + processos.cortes_apl + processos.negs_apl
    processos['Novos'] = horizonte * (PARAMETROS.alfa0*processos.notas_total + PARAMETROS.c*processos.cortes_apl +\
                                      PARAMETROS.t*processos.tois_apl + PARAMETROS.n*processos.negs_apl)
    print(processos)
    return processos



PREVALENCIAS, TOTAIS = calcula_prevalencias(carrega_dados())
PARAMETROS = carrega_parametros()

if __name__ == "__main__":
    import sys
    #dados = carrega_dados()
    #calcula_prevalencias(dados)
    #carrega_parametros()
    simula(int(sys.argv[1]), 1000, 1000, 1000)


