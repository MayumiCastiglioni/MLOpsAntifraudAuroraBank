import unittest
import pandas as pd
from sklearn.linear_model import LogisticRegression
from features import construir, carregar_contrato

class TestContratoPipeline(unittest.TestCase):
    def test_categoria_valida_ausente_no_treino(self):
        c=carregar_contrato()
        base={f["nome"]: (f["valores"][0] if f["tipo"]=="categoria" else max(f.get("min",0),1)) for f in c["features"]}
        X=pd.DataFrame([base]*4)
        p=construir(LogisticRegression(),c,True).fit(X,[0,1,0,1])
        novo=X.iloc[:1].copy();novo["uf_cliente"]="TO"
        self.assertEqual(p.predict_proba(novo).shape,(1,2))
