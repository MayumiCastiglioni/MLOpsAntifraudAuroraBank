"""Recalcula o relatório zero semanal a partir da referência E03 arquivada."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.contrato import carregar
from monitoramento import monitorar

RUN_ID = "ff48c43154624ec9a1e3d16688909ef3"
THRESHOLD = 0.10
LIMITE_KS = 0.10
LIMITE_TV = 0.10
SAIDA = ROOT / "docs/evidencias/relatorio-zero-semanas-11-12.json"


def gerar() -> dict:
    opcoes = [
        ROOT / "dados/referencia_e03_semanas_11_12.csv",
        ROOT / "artefatos/referencia_e03_semanas_11_12.csv",
    ]
    caminho = next((p for p in opcoes if p.is_file()), None)
    if caminho is None:
        raise FileNotFoundError("Referência E03 não encontrada em dados/ ou artefatos/.")

    referencia = pd.read_csv(caminho, sep=";", dtype={"id_transacao": str})
    semanas = set(pd.to_numeric(referencia["semana"], errors="raise").unique())
    if not {11, 12}.issubset(semanas):
        raise ValueError(f"Referência deve conter semanas 11 e 12; encontradas: {sorted(semanas)}")
    semana_11 = referencia.loc[referencia.semana == 11].copy()
    semana_12 = referencia.loc[referencia.semana == 12].copy()
    resultado = monitorar(
        semana_11, semana_12, carregar(), THRESHOLD, segmento="canal",
        rotulos_fechados=True, limite_ks=LIMITE_KS,
        limite_variacao_total=LIMITE_TV,
    )

    def registros(df: pd.DataFrame) -> list[dict]:
        # pandas converte NaN/inf para null de forma portável no JSON.
        return json.loads(df.to_json(orient="records", double_precision=15))

    alertas = registros(resultado["alertas"])
    disparados = [a for a in alertas if a["alerta"]]
    pacote = {
        "modelo_run_id": RUN_ID,
        "threshold": THRESHOLD,
        "semana_referencia": 11,
        "semana_lote": 12,
        "rotulos_fechados_confirmados": True,
        "n_referencia": len(semana_11),
        "n_lote": len(semana_12),
        "classificacao_variaveis": {
            "ks": [r["feature"] for r in registros(resultado["continuas"])],
            "proporcoes": sorted(set(r["feature"] for r in registros(resultado["categoricas"]))),
            "justificativa": "idade_conta_dias e qtd_transacoes_1h são ordinais numéricas; hora e dia da semana são distribuições cíclicas discretas.",
        },
        "limites": {
            "ks_D_gte": LIMITE_KS,
            "variacao_total_gte": LIMITE_TV,
            "interpretacao": "D=0,10 representa uma diferença máxima de 10 pontos percentuais entre CDFs; TV=0,10 representa pelo menos 10% de massa redistribuída. Limites heurísticos provisórios, não calibrados como taxas de falsos alertas.",
            "acao": "investigação humana; sem retreino ou alteração automática de modelo/threshold",
        },
        "continuas": registros(resultado["continuas"]),
        "categoricas": registros(resultado["categoricas"]),
        "alertas": alertas,
        "alertas_disparados": disparados,
        "operacional": registros(resultado["operacional"]),
        "performance": registros(resultado["performance"]),
        "resumo": {
            "n_alertas": len(disparados),
            "features_para_investigar": [a["feature"] for a in disparados],
            "limite_calibrado_em_historico_longo": False,
        },
        "metodo": "monitoramento.monitorar; KS para contínuas/score e ordinais numéricas; variação total para categorias, booleanas, hora e dia da semana",
        "referencia_arquivo": str(caminho.relative_to(ROOT)),
    }
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(pacote, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return pacote


if __name__ == "__main__":
    relatorio = gerar()
    print(json.dumps({
        "arquivo": str(SAIDA.relative_to(ROOT)),
        "semana_referencia": relatorio["semana_referencia"],
        "semana_lote": relatorio["semana_lote"],
        "n_alertas": relatorio["resumo"]["n_alertas"],
        "features_para_investigar": relatorio["resumo"]["features_para_investigar"],
    }, ensure_ascii=False, indent=2))
