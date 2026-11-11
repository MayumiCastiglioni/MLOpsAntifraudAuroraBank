"""Registra E03, valida o modelo versionado e promove champion após aprovação humana."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import mlflow
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient
import config

RUN_ID = "ff48c43154624ec9a1e3d16688909ef3"
THRESHOLD = 0.10
MOTIVO = "v1.0.0 - menor custo validado entre cinco famílias; promoção aprovada pela usuária em 10/11/2026"
DESCRICAO = ("RandomForestClassifier E03, RandomForest pipeline com pré-processamento do contrato v1.0. "
             "Threshold 0.10. Selecionado por menor custo nas semanas de validação 11-12: R$ 18.985,61 "
             "em duas semanas, contra R$ 225.349,79 da regra Pix > R$ 1.000. A validação foi usada na seleção; "
             "não é teste independente nem garantia de desempenho futuro.")


def main():
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    client = MlflowClient()
    run = client.get_run(RUN_ID)
    assert run.info.status == "FINISHED"
    assert round(run.data.metrics["custo"], 2) == 18985.61
    assert round(run.data.metrics["baseline_regra_pix"], 2) == 225349.79
    refs = {x.path for x in client.list_artifacts(RUN_ID, "referencia")}
    assert "referencia/referencia_e03_semanas_11_12.csv" in refs
    assert "referencia/referencia-e03-preparada.json" in refs

    try:
        model = client.get_registered_model(config.NOME_MODELO)
    except MlflowException as exc:
        if exc.error_code != "RESOURCE_DOES_NOT_EXIST":
            raise
        model = client.create_registered_model(config.NOME_MODELO)
    client.update_registered_model(config.NOME_MODELO, description="Modelo de bloqueio antifraude do Banco Aurora. Cada versão documenta algoritmo, contrato, threshold, evidência e motivo da decisão.")

    versions = client.search_model_versions(f"name='{config.NOME_MODELO}'")
    version = next((v for v in versions if v.run_id == RUN_ID), None)
    if version is None:
        version = client.create_model_version(name=config.NOME_MODELO, source=f"runs:/{RUN_ID}/modelo", run_id=RUN_ID, await_creation_for=300)
    version_id = str(version.version)
    client.set_model_version_tag(config.NOME_MODELO, version_id, config.TAG_THRESHOLD, str(THRESHOLD))
    client.set_model_version_tag(config.NOME_MODELO, version_id, config.TAG_MOTIVO, MOTIVO)
    client.set_model_version_tag(config.NOME_MODELO, version_id, "experimento_id", "E03")
    client.set_model_version_tag(config.NOME_MODELO, version_id, "decisao_custo", "semanas_11_12_validacao")
    client.update_model_version(config.NOME_MODELO, version_id, description=DESCRICAO)

    # Gate: carregar por número e confirmar artefato/signature antes de mover alias.
    candidato = mlflow.sklearn.load_model(f"models:/{config.NOME_MODELO}/{version_id}")
    origem = mlflow.sklearn.load_model(f"runs:/{RUN_ID}/modelo")
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    t = pd.read_csv(root/"dados/transacoes_semanas_01_12.csv", dtype={"id_transacao":str,"id_cliente":str})
    r = pd.read_csv(root/"dados/rotulos_semanas_01_12.csv", dtype={"id_transacao":str})
    df = t.merge(r,on="id_transacao",validate="one_to_one")
    valid = df[df.semana.eq(12)]
    cols = list(candidato.feature_names_in_)
    p1 = origem.predict_proba(valid[cols])[:,list(origem.classes_).index(1)]
    p2 = candidato.predict_proba(valid[cols])[:,list(candidato.classes_).index(1)]
    np.testing.assert_allclose(p1,p2,rtol=1e-12,atol=1e-12)

    anterior = None
    try:
        anterior = str(client.get_model_version_by_alias(config.NOME_MODELO,config.ALIAS_PRODUCAO).version)
    except MlflowException as exc:
        if exc.error_code != "RESOURCE_DOES_NOT_EXIST" and "alias" not in str(exc).lower():
            raise
    client.set_registered_model_alias(config.NOME_MODELO,config.ALIAS_PRODUCAO,version_id)
    ativo = client.get_model_version_by_alias(config.NOME_MODELO,config.ALIAS_PRODUCAO)
    assert str(ativo.version)==version_id
    assert ativo.tags.get(config.TAG_THRESHOLD)==str(THRESHOLD)
    evidence={"promovido_em_utc":datetime.now(timezone.utc).isoformat(),"modelo":config.NOME_MODELO,"alias":config.ALIAS_PRODUCAO,"versao":version_id,"versao_anterior":anterior,"run_id":RUN_ID,"threshold":THRESHOLD,"motivo":MOTIVO,"descricao":DESCRICAO,"paridade_com_run_semana_12":True,"n_transacoes_verificadas":len(valid),"referencia_artifacts":sorted(refs)}
    out=root/"docs/evidencias/promocao-e03.json"
    out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:evidence[k] for k in ["modelo","alias","versao","versao_anterior","run_id","threshold","paridade_com_run_semana_12"]},ensure_ascii=False))


if __name__=="__main__": main()
