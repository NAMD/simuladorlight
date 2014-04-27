#from django.test import TestCase
import unittest
from Interface.Simulador import carrega_parametros, calcula_prevalencias, carrega_dados, simula


class TestaSimulador(unittest.TestCase):
    def test_numero_de_parametros(self):
        par = carrega_parametros()
        self.assertEqual(len(par), 31)

    def testa_tamanho_tabela_prevalência(self):
        prev, tot = calcula_prevalencias(carrega_dados())
        self.assertEqual(len(prev), 31)
        self.assertEqual(len(tot), 31)

    def testa_prevalencias_somam_um(self):
        prev, tot = calcula_prevalencias(carrega_dados())
        self.assertAlmostEqual(prev.processo.sum(), 1, 3)
        self.assertAlmostEqual(prev.corte.sum(), 1, 3)
        self.assertAlmostEqual(prev.toi.sum(), 1, 3)
        self.assertAlmostEqual(prev.negativacao.sum(), 1, 3)
        self.assertAlmostEqual(prev.reclamacao.sum(), 1, 3)
        self.assertAlmostEqual(prev.toicorte.sum(), 1, 3)
        self.assertAlmostEqual(prev.toineg.sum(), 1, 3)

    def testa_soma_notas_isoladas(self):
        processos = simula(90, 1000, 1000, 1000)
        self.assertAlmostEqual(processos.tois_apl.sum(), 1000)
        self.assertAlmostEqual(processos.cortes_apl.sum(), 1000)
        self.assertAlmostEqual(processos.negs_apl.sum(), 1000)
        self.assertAlmostEqual(processos.sotois_apl.sum()+processos.sotn_apl.sum()+processos.sotc_apl.sum()+processos.tcn_apl.sum(), processos.tois_apl.sum())
        self.assertAlmostEqual(processos.socortes_apl.sum()+processos.socn_apl.sum()+processos.sotc_apl.sum()+processos.tcn_apl.sum(), processos.cortes_apl.sum())
        self.assertAlmostEqual(processos.sonegs_apl.sum()+processos.socn_apl.sum()+processos.sotn_apl.sum()+processos.tcn_apl.sum(), processos.negs_apl.sum())
       # self.assertAlmostEqual(processos.sotois_apl.sum()+processos.socortes_apl.sum()+processos.sotc_apl.sum()+\
       #                        processos.sonegs_apl.sum()+processos.sotn_apl.sum()+processos.tcn_apl.sum()+\
       #                        processos.socn_apl.sum(), processos.tois_apl.sum()+processos.cortes_apl.sum()+processos.negs_apl.sum(), 1)



