import unittest
import numpy as np
import pandas as pd
from monitoramento import drift_continuas, drift_categoricas, saida_operacional, performance_rotulada, monitorar

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
    def test_monitorar_consolida_alertas_no_limite(self):
        contrato={'features':[{'nome':'x','tipo':'float'},{'nome':'canal','tipo':'categoria'}]}
        ref=pd.DataFrame({'x':[0.,0.], 'canal':['pix','pix'], 'score':[.2,.8],
                          'valor_transacao':[100.,100.], 'fraude':[0,1]})
        lote=pd.DataFrame({'x':[1.,1.], 'canal':['online','online'], 'score':[.2,.8],
                           'valor_transacao':[100.,100.], 'fraude':[0,1]})
        resultado=monitorar(ref,lote,contrato,.5,limite_ks=1.,limite_variacao_total=1.)
        alertas=resultado['alertas'].set_index('feature')
        self.assertEqual(set(resultado),{'continuas','categoricas','alertas','operacional','performance'})
        for feature, medida in [('x','D'),('canal','variacao_total')]:
            with self.subTest(feature=feature):
                linha=alertas.loc[feature]
                self.assertEqual(linha['medida'],medida)
                self.assertEqual(linha['valor'],1.)
                self.assertEqual(linha['limite'],1.)
                self.assertTrue(linha['alerta'])
                self.assertEqual(linha['acao'],'investigar')
                self.assertEqual(linha['status'],'calculado')
    def test_sem_amostra_valida_pede_verificacao_de_qualidade(self):
        contrato={'features':[{'nome':'x','tipo':'float'},{'nome':'canal','tipo':'categoria'}]}
        ref=pd.DataFrame({'x':[np.nan,np.inf], 'canal':['pix','online'], 'score':[.2,.8],
                          'valor_transacao':[100.,100.], 'fraude':[0,1]})
        lote=ref.copy()
        resultado=monitorar(ref,lote,contrato,.5)
        for relatorio in [resultado['continuas'].set_index('feature'),
                          resultado['alertas'].set_index('feature')]:
            linha=relatorio.loc['x']
            self.assertEqual(linha['status'],'sem_amostra_valida')
            self.assertFalse(linha['alerta'])
            self.assertEqual(linha['acao'],'verificar_qualidade_dados')
    def test_inteiros_ordinais_encaminhados_para_ks(self):
        contrato={'features':[{'nome':'idade_conta_dias','tipo':'int'},
                              {'nome':'qtd_transacoes_1h','tipo':'int'},
                              {'nome':'canal','tipo':'categoria'}]}
        ref=pd.DataFrame({'idade_conta_dias':[1,2], 'qtd_transacoes_1h':[3,4],
                          'canal':['pix','online'], 'score':[.2,.8],
                          'valor_transacao':[100.,100.], 'fraude':[0,1]})
        lote=ref.copy()
        resultado=monitorar(ref,lote,contrato,.5)
        nomes_ks=set(resultado['continuas']['feature'])
        self.assertTrue({'idade_conta_dias','qtd_transacoes_1h'}.issubset(nomes_ks))
        alertas=resultado['alertas'].set_index('feature')
        for feature in ['idade_conta_dias','qtd_transacoes_1h']:
            self.assertEqual(alertas.loc[feature,'tipo'],'ks')
    def test_sem_fraude_indefinido(self):
        df=self.df.fillna({'fraude':0}).assign(fraude=0)
        r=performance_rotulada(df,.5).iloc[0]
        self.assertTrue(np.isnan(r.recall))
        self.assertTrue(np.isnan(r.average_precision))
    def test_rotulo_invalido(self):
        with self.assertRaises(ValueError):performance_rotulada(self.df.assign(fraude=2),.5)
