import unittest
from monitoramento import custo, medir

class TestCusto(unittest.TestCase):
    def test_assimetria(self):
        self.assertEqual(custo([1,0,1,0],[0,1,1,0],[200,100,300,50]),215)
    def test_sem_rotulo(self):
        with self.assertRaises(ValueError): custo([float("nan")],[0],[10])
    def test_aprovar_tudo(self):
        self.assertEqual(custo([1,0],[0,0],[200,100]),200)
    def test_bloquear_tudo(self):
        self.assertEqual(custo([1,0],[1,1],[200,100]),15)

    def test_igual_threshold_bloqueia(self):
        self.assertEqual(medir([0],[0.1],[100],0.1)["custo"],15)
    def test_score_ausente(self):
        with self.assertRaises(ValueError): medir([1],[float("nan")],[100],0.1)
