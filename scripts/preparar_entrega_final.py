"""Cria um pacote integral da atividade sem sobrescrever entregas anteriores."""
from __future__ import annotations

import hashlib
import argparse
import json
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from mlflow.tracking import MlflowClient

import config
from app.contrato import nomes_features, tipar


RUN_ID_ESPERADO = "ff48c43154624ec9a1e3d16688909ef3"
NOME_ALUNO = "Mayumi Castiglioni"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def copiar_arquivo(destino: Path, relativo: str, nome: str | None = None) -> Path:
    origem = ROOT / relativo
    if not origem.is_file():
        raise FileNotFoundError(f"Arquivo necessário não encontrado: {relativo}")
    alvo = destino / (nome or relativo)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origem, alvo)
    return alvo


def preparar() -> tuple[Path, Path, dict]:
    agora = datetime.now(timezone.utc)
    id_execucao = agora.strftime("%Y%m%dT%H%M%SZ")
    pasta = ROOT / "entrega" / f"parte1_final_{id_execucao}"
    pasta.mkdir(parents=True, exist_ok=False)
    avisos: list[str] = []

    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    cliente = MlflowClient()
    champion = cliente.get_model_version_by_alias(config.NOME_MODELO, config.ALIAS_PRODUCAO)
    run = cliente.get_run(champion.run_id)
    caminhos_referencia = [a.path for a in cliente.list_artifacts(champion.run_id, "referencia")]
    if str(champion.run_id) != RUN_ID_ESPERADO:
        avisos.append(f"run do champion difere da run aprovada: {champion.run_id}")
    if champion.tags.get(config.TAG_THRESHOLD) != "0.1":
        avisos.append(f"threshold inesperado na versão: {champion.tags.get(config.TAG_THRESHOLD)}")
    if not champion.tags.get(config.TAG_MOTIVO) or not champion.description:
        avisos.append("versão champion sem motivo ou descrição")
    if not any("referencia_e03_semanas_11_12.csv" in x for x in caminhos_referencia):
        avisos.append("artefato CSV de referência não foi encontrado na run champion")

    # Salva uma cópia local do modelo registrado e dos artefatos de referência.
    modelo_destino = pasta / "modelo_exportado"
    modelo_destino.mkdir()
    caminho_modelo = mlflow.artifacts.download_artifacts(
        artifact_uri=f"models:/{config.NOME_MODELO}/{champion.version}",
        dst_path=str(modelo_destino),
    )
    # A run contém cópias de toda a documentação histórica. O pacote já inclui
    # essa documentação versionada; copie apenas a referência efetiva para
    # evitar caminhos excessivos em instalações Windows.
    ref_destino = pasta / "referencia"
    ref_destino.mkdir()
    referencia_local = ROOT / "artefatos/referencia_e03_semanas_11_12.csv"
    shutil.copy2(referencia_local, ref_destino / referencia_local.name)
    shutil.copy2(ROOT / "docs/evidencias/referencia-e03-preparada.json",
                 ref_destino / "referencia-e03-preparada.json")
    manifesto_ref = json.loads((ROOT / "docs/evidencias/referencia-e03-preparada.json").read_text(encoding="utf-8"))
    if sha256(referencia_local) != manifesto_ref["linhagem"]["referencia_sha256"]:
        avisos.append("SHA-256 da referência local diverge do manifesto validado")

    # Confere serviço e paridade no momento em que o pacote é montado.
    status_api_modelo: dict = {}
    try:
        with urllib.request.urlopen(f"{config.SISTEMA_URL}/saude", timeout=10) as resposta:
            saude = json.loads(resposta.read().decode("utf-8"))
        with urllib.request.urlopen(f"{config.SISTEMA_URL}/api/modelo", timeout=10) as resposta:
            status_api_modelo = json.loads(resposta.read().decode("utf-8"))
        status_modelo = saude.get("modelo", {})
        if str(status_modelo.get("versao")) != str(champion.version):
            avisos.append("API e alias champion apontam para versões diferentes")
        if not status_modelo.get("ok"):
            avisos.append("API reportou modelo indisponível")
        if (str(status_api_modelo.get("modelo", {}).get("versao")) != str(champion.version)
                or float(status_api_modelo.get("modelo", {}).get("threshold", -1))
                != float(champion.tags.get(config.TAG_THRESHOLD, -2))):
            avisos.append("página Modelo da API e alias champion divergem")

        contrato = yaml.safe_load((ROOT / "contrato/contrato_features.yaml").read_text(encoding="utf-8"))
        features = nomes_features(contrato)
        dados = pd.read_csv(ROOT / "dados/transacoes_semanas_01_12.csv")
        amostra = dados.loc[dados.semana == 12, features].head(5).copy()
        modelo = mlflow.sklearn.load_model(f"models:/{config.NOME_MODELO}/{champion.version}")
        scores_locais = modelo.predict_proba(tipar(amostra, contrato))[:, 1]
        payload = json.loads(amostra.to_json(orient="records"))
        request = urllib.request.Request(
            f"{config.SISTEMA_URL}/predict",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as resposta:
            previsoes_api = json.loads(resposta.read().decode("utf-8"))
        threshold = float(champion.tags[config.TAG_THRESHOLD])
        paridade = len(previsoes_api) == 5 and all(
            abs(item["score"] - round(float(score), 6)) < 1e-12
            and item["bloquear"] == (float(score) >= threshold)
            and str(item["versao_modelo"]) == str(champion.version)
            for item, score in zip(previsoes_api, scores_locais)
        )
        if not paridade:
            avisos.append("paridade de API não confirmada para as cinco transações")
    except Exception as erro:  # a evidência fica explícita no manifesto da entrega
        saude = {"erro": f"{type(erro).__name__}: {erro}"}
        paridade = False
        avisos.append("não foi possível verificar a API durante a exportação")

    arquivos = [
        ("README.md", None), ("CHANGELOG.md", None), ("CONTRIBUTING.md", None),
        ("parte1.ipynb", None), ("notebooks/01_analise_e_escolha.ipynb", None),
        ("config.py", None), (".env.exemplo", ".env.exemplo"),
        ("features.py", None), ("monitoramento.py", None),
        ("requirements.txt", None),
        ("contrato/contrato_features.yaml", "contrato/contrato_features.yaml"),
        ("dados/transacoes_semanas_01_12.csv", "dados/transacoes_semanas_01_12.csv"),
        ("dados/rotulos_semanas_01_12.csv", "dados/rotulos_semanas_01_12.csv"),
        ("artefatos/referencia_e03_semanas_11_12.csv", "dados/referencia_e03_semanas_11_12.csv"),
    ]
    arquivos_incluidos = [copiar_arquivo(pasta, origem, nome) for origem, nome in arquivos]
    for diretorio in ("app", "sql", "scripts", "docs", "tests"):
        origem = ROOT / diretorio
        shutil.copytree(origem, pasta / diretorio, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    # Preserve outputs from the latest full notebook reproduction, including
    # the five model result files, threshold curves, data hashes, and summary.
    evidencia_repro = ROOT / "docs/evidencias/notebook-reproduzido.json"
    resumo_reproducao: Path | None = None
    if evidencia_repro.exists():
        reproducao = json.loads(evidencia_repro.read_text(encoding="utf-8"))
        origem_resultados = ROOT / reproducao["pasta"]
        dentro_do_projeto = origem_resultados.resolve().is_relative_to(ROOT.resolve())
        if (origem_resultados.is_dir() and dentro_do_projeto
                and (origem_resultados / "manifesto.json").is_file()
                and (origem_resultados / "resultados.json").is_file()):
            destino_resultados = pasta / "resultados_reproducao" / origem_resultados.name
            shutil.copytree(origem_resultados, destino_resultados)
            resumo_reproducao = origem_resultados / "RESUMO_ESCOLHA.md"
            # Store paths relative to the extracted ZIP, not to the author's workspace.
            reproducao["pasta"] = (Path("resultados_reproducao") / origem_resultados.name).as_posix()
            reproducao["resultados"] = (Path("resultados_reproducao") / origem_resultados.name).as_posix()
            (pasta / "docs/evidencias/notebook-reproduzido.json").write_text(
                json.dumps(reproducao, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        else:
            avisos.append("resultados da última execução reproduzível não foram encontrados dentro do projeto")
    else:
        avisos.append("manifesto da última execução reproduzível não foi encontrado")

    if resumo_reproducao and resumo_reproducao.is_file():
        shutil.copy2(resumo_reproducao, pasta / "RESUMO_ESCOLHA.md")
    else:
        avisos.append("resumo da reprodução não foi encontrado dentro dos resultados arquivados")

    leia_primeiro = """# Entrega final — Banco Aurora\n\nAutora: Mayumi Castiglioni. O pacote reúne notebook da atividade, notebook executado de auditoria e comparação, resultados e curvas das cinco famílias, código, contrato, dados fornecidos, referência e evidências da versão promovida.\n\n## Ordem de leitura\n\n1. `parte1.ipynb` — respostas, evidências e verificação de operação.\n2. `RESUMO_ESCOLHA.md` — escolha em linguagem de custo.\n3. `resultados_reproducao/` — métricas, curvas, hashes, run_ids e resumo da reprodução integral.\n4. `docs/decisoes/` e `docs/evidencias/` — decisões e rastreabilidade.\n\n## Reprodução\n\nUse Python 3.11 e instale `requirements.txt`. Para reproduzir análise e treinos, abra `notebooks/01_analise_e_escolha.ipynb` e execute todas as células. Para refazer as conferências de produção no notebook `parte1.ipynb`, configure `.env` a partir de `.env.exemplo`, inicie Postgres, MLflow e API conforme `docs/reproducao-e-entrega.md` e execute as células. A promoção de modelo não é automática.\n\nOs resultados das semanas 11–12 são validação usada na seleção, não teste independente. A política de alerta gera investigação humana; não retreina nem troca modelo ou corte automaticamente.\n"""
    (pasta / "README.md").write_text(leia_primeiro, encoding="utf-8")

    resultado = {
        "aluno": NOME_ALUNO,
        "gerado_em_utc": agora.isoformat(timespec="seconds"),
        "modelo": config.NOME_MODELO,
        "alias": config.ALIAS_PRODUCAO,
        "versao": str(champion.version),
        "run_id": champion.run_id,
        "tags_versao": dict(champion.tags),
        "descricao": champion.description,
        "params_run": run.data.params,
        "metricas_run": run.data.metrics,
        "referencia_mlflow": caminhos_referencia,
        "modelo_exportado": str(Path(caminho_modelo).relative_to(pasta)),
        "api_versao_confirmada": str(saude.get("modelo", {}).get("versao", "")),
        "api_pagina_modelo": status_api_modelo,
        "paridade_api_5_transacoes": bool(paridade),
        "arquivos_dados_sha256": {str(p.relative_to(pasta)): sha256(p) for p in arquivos_incluidos if "dados" in p.parts},
        "avisos": avisos,
    }
    (pasta / "VERIFICACAO_ENTREGA.json").write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    zip_path = ROOT / f"entrega_parte1_mayumi_castiglioni_{id_execucao}.zip"
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", root_dir=pasta)
    resultado["pasta"] = str(pasta.relative_to(ROOT))
    resultado["zip"] = str(zip_path.relative_to(ROOT))
    resultado["zip_bytes"] = zip_path.stat().st_size
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    return pasta, zip_path, resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="confere os pré-requisitos sem criar arquivos")
    args = parser.parse_args()
    if args.check_only:
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        client = MlflowClient()
        current = client.get_model_version_by_alias(config.NOME_MODELO, config.ALIAS_PRODUCAO)
        with urllib.request.urlopen(f"{config.SISTEMA_URL}/saude", timeout=10) as response:
            health = json.loads(response.read().decode("utf-8"))
        checks = {
            "champion_v1": str(current.version) == "1",
            "threshold_0_10": current.tags.get(config.TAG_THRESHOLD) == "0.1",
            "motivo_e_descricao": bool(current.tags.get(config.TAG_MOTIVO) and current.description),
            "referencia_na_run": any("referencia_e03_semanas_11_12.csv" in x for x in
                                     [a.path for a in client.list_artifacts(current.run_id, "referencia")]),
            "api_servindo_mesma_versao": str(health.get("modelo", {}).get("versao")) == str(current.version),
            "pagina_modelo_mesma_versao_e_corte": False,
            "dados_locais_disponiveis": (ROOT / "dados/transacoes_semanas_01_12.csv").is_file()
                                         and (ROOT / "dados/rotulos_semanas_01_12.csv").is_file(),
            "resultados_reproducao_disponiveis": (ROOT / "docs/evidencias/notebook-reproduzido.json").is_file(),
        }
        with urllib.request.urlopen(f"{config.SISTEMA_URL}/api/modelo", timeout=10) as response:
            api_model = json.loads(response.read().decode("utf-8"))
        checks["pagina_modelo_mesma_versao_e_corte"] = (
            str(api_model.get("modelo", {}).get("versao")) == str(current.version)
            and float(api_model.get("modelo", {}).get("threshold", -1)) == float(current.tags[config.TAG_THRESHOLD])
        )
        print(json.dumps({"pre_requisitos_ok": all(checks.values()), "checks": checks}, indent=2, ensure_ascii=False))
        if not all(checks.values()):
            raise SystemExit(1)
    else:
        preparar()
