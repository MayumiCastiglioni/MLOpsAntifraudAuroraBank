import unittest
from monitoramento import custo

class TestCusto(unittest.TestCase):
    def test_assimetria(self):
        self.assertEqual(custo([1,0,1,0],[0,1,1,0],[200,100,300,50]),215)
    def test_sem_rotulo(self):
        with self.assertRaises(ValueError): custo([float("nan")],[0],[10])
    def test_aprovar_tudo(self):
        self.assertEqual(custo([1,0],[0,0],[200,100]),200)
    def test_bloquear_tudo(self):
        self.assertEqual(custo([1,0],[1,1],[200,100]),15)
