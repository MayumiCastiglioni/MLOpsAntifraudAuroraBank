"""Reconstrói a referência E03 local; não escreve no MLflow/backend."""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score
import config
from features import carregar_contrato
from monitoramento import medir

RUN = "ff48c43154624ec9a1e3d16688909ef3"
THRESHOLD = 0.10
ARTIFATO = Path.home() / ".codex" / "aurora-artifacts" / RUN / "artifacts" / "modelo"


def main():
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    modelo = mlflow.sklearn.load_model(str(ARTIFATO))
    cols = [f["nome"] for f in carregar_contrato()["features"]]
    trans_path = ROOT / "dados" / "transacoes_semanas_01_12.csv"
    rotulos_path = ROOT / "dados" / "rotulos_semanas_01_12.csv"
    t = pd.read_csv(trans_path, dtype={"id_transacao": str, "id_cliente": str})
    r = pd.read_csv(rotulos_path, dtype={"id_transacao": str})
    dados = t.merge(r, on="id_transacao", validate="one_to_one")
    validacao = dados[dados.semana.isin([11, 12])].copy()
    assert len(validacao) == 39497 and len(cols) == 13
    score = modelo.predict_proba(validacao[cols])[:, list(modelo.classes_).index(1)]
    validacao["score"] = score
    validacao["bloqueada"] = score >= THRESHOLD
    referencia = validacao[["id_transacao", "semana"] + cols + ["score", "bloqueada", "fraude"]]
    destino = ROOT / "artefatos" / "referencia_e03_semanas_11_12.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    referencia.to_csv(destino, index=False, sep=";", float_format="%.12g")
    check = pd.read_csv(destino, sep=";", dtype={"id_transacao": str})
    assert len(check) == 39497 and check.id_transacao.is_unique
    metricas = {}
    for semana in (11, 12):
        grupo = check[check.semana == semana]
        metricas[str(semana)] = {"n": len(grupo), **medir(grupo.fraude, grupo.score, grupo.valor_transacao, THRESHOLD), "accuracy": float(accuracy_score(grupo.fraude, grupo.bloqueada))}
    assert round(metricas["11"]["custo"], 2) == 11019.25
    assert round(metricas["12"]["custo"], 2) == 7966.36
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifesto = {"run_id": RUN, "modelo": "E03 RandomForestClassifier", "threshold": THRESHOLD, "semanas": [11, 12], "linhas": len(check), "features": cols, "linhagem": {"transacoes_sha256": sha(trans_path), "rotulos_sha256": sha(rotulos_path), "referencia_sha256": sha(destino)}, "metricas_por_semana": metricas, "status": "preparada_e_validada_localmente; anexar à run E03 quando Postgres/MLflow voltar"}
    saida = ROOT / "docs" / "evidencias" / "referencia-e03-preparada.json"
    saida.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"csv": str(destino), "manifesto": str(saida), "n": len(check), "metricas": metricas}, ensure_ascii=False))


if __name__ == "__main__":
    main()
