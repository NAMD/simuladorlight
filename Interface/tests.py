#from django.test import TestCase
import unittest
from Interface.Simulador import carrega_parametros, calcula_prevalencias, carrega_dados


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



