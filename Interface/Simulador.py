#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def carrega_dados():
    """
    Lê os dados brutos.
    :rtype : pd.DataFrame
    """
    df = pd.read_csv('Interface/tabelaparaosimulador.csv.gz',
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
    # Binariza os dados
    for n in dados.columns:
        if n.startswith("data_") or n == "contrato":
            dados[n] = pd.notnull(dados[n])
            dados[n].astype(int)
    # cria colunas para os termos de interação
    dados["_toicorte"] = dados.data_toi & dados.data_corte
    dados["_toineg"] = dados.data_toi & dados.data_negativacao
    dados["_toirec"] = dados.data_toi & dados.data_reclamacao
    dados["_corteneg"] = dados.data_corte & dados.data_negativacao
    dados["_corterec"] = dados.data_corte & dados.data_reclamacao
    dados["_negrec"] = dados.data_negativacao & dados.data_reclamacao
    dados["_toicorteneg"] = dados.data_toi & dados.data_corte & dados.data_negativacao
    dados["_toicorterec"] = dados.data_toi & dados.data_corte & dados.data_reclamacao
    dados["_toinegrec"] = dados.data_toi & dados.data_negativacao & dados.data_reclamacao
    dados["_cortenegrec"] = dados.data_corte & dados.data_negativacao & dados.data_reclamacao

    del dados['dt_inicio'], dados['dt_fim']
    totais = dados.groupby(level=0).sum()
    # Adicionando novas colunas
    totais["sem_nota"] = totais.contrato - (
    totais.data_corte + totais.data_toi + totais.data_negativacao + totais.data_reclamacao)

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
    parametros = pd.read_csv("Interface/alphas-weibull.csv", index_col=0, header=0)
    #print(parametros[:10])
    return parametros


def distribui_notas(ncorte, nneg, ntoi, processos):
    """
    Distribui Notas de acordo com suas prevalências nos municípios
    :param ncorte: Numero total de notas de corte
    :param nneg: Numero total de notas de negativação
    :param ntoi: Numero total de notas de toi
    :param processos: DataFrame com indice de municípios e seus geocódigos
    :return: Dataframe com as notas distribuídas
    """
    # Primeiro calculo o tcn pois não precisa descontar nada
    processos["tcn_apl"] = (ntoi + ncorte + nneg) * PREVALENCIAS.toicorteneg
    # no calculo do número de só TN temos que descontar tcn que é contado duas vezes
    processos["sotn_apl"] = (ntoi + nneg) * PREVALENCIAS.toineg - processos.tcn_apl
    # no calculo do número de só TC temos que descontar tcn que é contado duas vezes
    processos["sotc_apl"] = (ntoi + ncorte) * PREVALENCIAS.toicorte - processos.tcn_apl
    # no calculo do número de só CN temos que descontar tcn que é contado duas vezes
    processos["socn_apl"] = (ncorte + nneg) * PREVALENCIAS.corteneg
    # No cálculo de só Toi precisamos descontar só toicorte, só toineg e tcn
    processos["sotois_apl"] = ntoi * PREVALENCIAS.toi - (processos.sotc_apl + processos.sotn_apl + processos.tcn_apl)
    # No cálculo de só Toi precisamos descontar só toicorte, só toineg e tcn
    processos["socortes_apl"] = ncorte * PREVALENCIAS.corte - (
    processos.sotc_apl + processos.socn_apl + processos.tcn_apl)
    # No cálculo de só Neg precisamos descontar só corteneg, só toineg e tcn
    processos["sonegs_apl"] = nneg * PREVALENCIAS.negativacao - (
    processos.sotn_apl + processos.socn_apl + processos.tcn_apl)

    processos["tois_apl"] = ntoi * PREVALENCIAS.toi
    processos["cortes_apl"] = ncorte * PREVALENCIAS.corte
    processos["negs_apl"] = nneg * PREVALENCIAS.negativacao
    processos["tc_apl"] = (ntoi + ncorte) * PREVALENCIAS.toicorte
    processos["tn_apl"] = (ntoi + nneg) * PREVALENCIAS.toineg
    #processos["tr_apl"] = (ntoi+nrec)
    processos["cn_apl"] = (ncorte + nneg) * PREVALENCIAS.corteneg

    return processos


def simula(horizonte=30, ntoi=0, ncorte=0, nneg=0):
    """
    Esta função calcula o número esperado de processos judiciais com base no estado atual do sistema e o número de
    notas a serem aplicadas. A notas são distribuídas por todos os municípios.
    :param horizonte: Horizonte de previsão em dias
    :param ntoi: Numero de novos tois a serem aplicados
    :param ncorte: Numero de novos cortes a serem aplicados
    :param nneg: Número de negativações a serem aplicados
    """
    processos = pd.DataFrame(index=PARAMETROS.index.tolist())
    processos['geocodigo'] = PARAMETROS.geocodigo

    # Distribuindo as notas por municipio de acordo com as prevalencias
    processos = distribui_notas(ncorte, nneg, ntoi, processos)
    total_notas = processos.tois_apl + processos.cortes_apl + processos.negs_apl
    processos['notas_total'] = processos.tois_apl + processos.cortes_apl + processos.negs_apl
    processos['Novos'] = total_notas - total_notas * np.exp(
        -horizonte * (PARAMETROS.intercept + PARAMETROS.c * processos.cortes_apl + \
                      PARAMETROS.t * processos.tois_apl + PARAMETROS.n * processos.negs_apl + \
                      PARAMETROS.tc * processos.tc_apl + PARAMETROS.tn * processos.tn_apl + \
                      PARAMETROS.cn * processos.cn_apl + PARAMETROS.tcn * processos.tcn_apl))
    #print(processos)
    #print(processos.Novos.sum())
    return processos


def simula_municipio(horizonte=30, ntoi=0, ncorte=0, nneg=0, municipio=3304557):
    """
    Esta função calcula o número esperado de processos judiciais com base no estado atual do sistema e o número de
    notas a serem aplicadas. Todas as notas são direcionadas a um município.
    :param horizonte: Horizonte de previsão em dias
    :param ntoi: Numero de novos tois a serem aplicados
    :param ncorte: Numero de novos cortes a serem aplicados
    :param nneg: Número de negativações a serem aplicados
    """
    parametros = PARAMETROS.set_index("geocodigo")

    PAR = parametros.ix[municipio]

    total_notas = ntoi + ncorte + nneg

    processos = total_notas - total_notas * np.exp(
        -horizonte * (PAR.intercept + PAR.c * ncorte + PAR.t * ntoi + PAR.n * nneg + \
                      PAR.tc * (ntoi + ncorte) + PAR.tn * (ntoi + nneg) + \
                      PAR.cn * (ncorte + nneg) + PAR.tcn * (ntoi + ncorte + nneg)))

    return processos


PREVALENCIAS, TOTAIS = calcula_prevalencias(carrega_dados())
PARAMETROS = carrega_parametros()

if __name__ == "__main__":
    import sys
    #dados = carrega_dados()
    #calcula_prevalencias(dados)
    #carrega_parametros()
    simula(int(sys.argv[1]), 1000, 1000, 1000)


