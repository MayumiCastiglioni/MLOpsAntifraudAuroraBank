import unittest
import numpy as np
import pandas as pd
from monitoramento import drift_continuas, drift_categoricas, saida_operacional, performance_rotulada

class TestMonitoramento(unittest.TestCase):
    def setUp(self):
        self.df=pd.DataFrame(dict(score=[.1,.9,.8],valor_transacao=[100,200,300],fraude=[0,1,np.nan],canal=["pix","pix","online"]))
    def test_sem_rotulo_nao_vira_zero(self):
        r=performance_rotulada(self.df,.5).iloc[0]
        self.assertEqual(r.rotuladas,2)
        self.assertAlmostEqual(r.cobertura,2/3)
        self.assertEqual(r.custo_observado,0)
        self.assertTrue(np.isnan(r.custo_final))
    def test_fechamento_explicito(self):
        df=self.df.fillna({"fraude":1})
        self.assertTrue(np.isnan(performance_rotulada(df,.5).iloc[0].custo_final))
        self.assertEqual(performance_rotulada(df,.5,rotulos_fechados=True).iloc[0].custo_final,0)
    def test_sem_rotulos(self):
        r=performance_rotulada(self.df.drop(columns="fraude"),.5).iloc[0]
        self.assertEqual(r.status,"sem_rotulos")
        self.assertTrue(np.isnan(r.recall))
    def test_operacao_sem_rotulos(self):
        r=saida_operacional(self.df,.8).iloc[0]
        self.assertEqual(r.bloqueadas,2)
        self.assertEqual(r.valor_bloqueado,500)
    def test_categoria_nova_e_ausente(self):
        a=pd.DataFrame({'x':['a','a']});b=pd.DataFrame({'x':['b',None]})
        r=drift_categoricas(a,b,['x'])
        self.assertEqual(r.variacao_total.iloc[0],1)
        self.assertEqual(r.categoria_nova.sum(),2)
    def test_ks_sem_mudanca_e_invalidos(self):
        a=pd.DataFrame({'x':[1,2,3,np.nan]})
        r=drift_continuas(a,a,['x']).iloc[0]
        self.assertEqual(r.D,0)
        self.assertEqual(r.invalidos_lote,1)
    def test_sem_fraude_indefinido(self):
        df=self.df.fillna({'fraude':0}).assign(fraude=0)
        r=performance_rotulada(df,.5).iloc[0]
        self.assertTrue(np.isnan(r.recall))
        self.assertTrue(np.isnan(r.average_precision))
    def test_rotulo_invalido(self):
        with self.assertRaises(ValueError):performance_rotulada(self.df.assign(fraude=2),.5)
