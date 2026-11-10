"""Atualiza relatório e notebook com evidências reais, sem promover ou retreinar."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import nbformat
import mlflow
import config


def main():
    registros=json.loads(Path("docs/evidencias/experimentos-iniciais.json").read_text(encoding="utf-8"))
    completos=[r for r in registros if r["status"]=="concluido"]
    if len(registros)!=5 or len(completos)!=5: raise RuntimeError("A rodada ainda não terminou com cinco resultados")
    vencedor=min(completos,key=lambda r:r["resultado"]["custo"])
    linhas=["| ID | Algoritmo | Corte | Custo 11–12 (R$) | Recall | Precision | Average precision |", "|---|---|---|---|---|---|---|"]
    for r in completos:
        m=r["resultado"]
        linhas.append(f"| {r['id']} | {r['algoritmo']} | {m['threshold']:.2f} | {m['custo']:.2f} | {m['recall']:.4f} | {m['precision']:.4f} | {m['average_precision']:.4f} |")
    tabela="\n".join(linhas)
    m=vencedor["resultado"];b=vencedor["baselines"]
    justificativa=f"Escolha para a próxima etapa: {vencedor['id']} ({vencedor['algoritmo']}), corte {m['threshold']:.2f}, pelo menor custo agregado observado. Custo total de R$ {m['custo']:.2f} em duas semanas, média de R$ {m['custo']/2:.2f}/semana. Economia contra a regra Pix: R$ {b['regra_pix']-m['custo']:.2f} ({100*(1-m['custo']/b['regra_pix']):.2f}%). Legítimas bloqueadas: {m['legitimas_bloqueadas']} transações (não clientes únicos). Fraude monetária aprovada: R$ {m['fraude_perdida']:.2f}."
    semana="\n".join(f"- Semana {x['semana']}: custo R$ {x['custo']:.2f}; {x['legitimas_bloqueadas']} legítimas bloqueadas; fraude perdida R$ {x['fraude_perdida']:.2f}." for x in vencedor["semanas"])
    limites="A seleção e o corte usam as semanas 11–12: são validação, não teste independente nem garantia futura. A promoção E03, o monitoramento baseline, o registro de versão, a paridade de API e o pacote final foram concluídos depois e estão documentados em docs/decisoes/ e docs/evidencias/. O threshold global simplifica custos que variam com o valor da transação."
    pisos="\n".join(f"- {k}: R$ {v:.2f}." for k,v in b.items())
    motivos="\n".join(f"- {r['id']}: {'selecionado pelo menor custo' if r['id']==vencedor['id'] else 'não selecionado nesta rodada: custo superior ao escolhido'}; run `{r['run_id']}`; treino {r['treino_segundos']:.2f}s; inferência de 39.497 transações {r['inferencia_segundos']:.3f}s." for r in completos)
    report=f"# Comparação inicial e escolha fundamentada\n\nRodada executada em 06/11/2026, configurações definidas previamente em docs/experimentos.md.\n\n{tabela}\n\n## Escolha\n\n{justificativa}\n\n{semana}\n\n## Baselines agregados do selecionado\n\n{pisos}\n\n## Tentativas e descartes\n\n{motivos}\n\nTentativa técnica anterior E01: falha antes do treino por URI de artefatos e codificação do console; registro preservado em tentativa-tecnica-inicial.json. Não é evidência contra o algoritmo.\n\n## Limitações\n\n{limites}\n\n![Curvas de custo](custo-por-threshold.png)\n"
    interpretacao=Path("docs/interpretacao-comparacao.md")
    if interpretacao.exists(): report += "\n\n"+interpretacao.read_text(encoding="utf-8")
    Path("docs/evidencias/comparacao-inicial.md").write_text(report,encoding="utf-8")
    Path("docs/decisoes/004-escolha-inicial.md").write_text("# 004 — Escolha após rodada inicial\n\nData: 06/11/2026. Estado: aceita para selecionar candidato; promoção pendente.\n\n"+justificativa+"\n\nAlternativas: cinco famílias do protocolo. Evidência: docs/evidencias/experimentos-iniciais.json, curvas e runs listadas no relatório.\n\n"+semana+"\n\n"+limites,encoding="utf-8")
    nb=nbformat.read("material/antifraude_mlops/parte1.ipynb",as_version=4)
    extras={
      "## 1.":[nbformat.v4.new_markdown_cell(Path("docs/evidencias/auditoria-inicial.md").read_text(encoding="utf-8")),nbformat.v4.new_code_cell("import json\nfrom pathlib import Path\nauditoria = json.loads(Path('docs/evidencias/auditoria-inicial.json').read_text(encoding='utf-8'))\nprint(auditoria['juncao'])")],
      "## 2.":[nbformat.v4.new_markdown_cell("Usamos 200.887 transações das semanas 1–10 para treino e 39.497 de 11–12 para validação. Uma divisão aleatória misturaria futuro e passado, contrariaria a tarefa e enfraqueceria a simulação de operação futura. Clientes podem reaparecer; IDs não são features. Taxas semanais e intervalos estão nos relatórios de auditoria." )],
      "## 3.":[nbformat.v4.new_code_cell("from features import construir, carregar_contrato\ncontrato = carregar_contrato()\nprint([f['nome'] for f in contrato['features']])")],
      "## 4.":[nbformat.v4.new_markdown_cell(Path("docs/experimentos.md").read_text(encoding="utf-8")),nbformat.v4.new_code_cell("# Rodada já executada; este bloco consulta evidências, sem retreinar.\n# Reprodução completa: python scripts/executar_experimentos.py\nimport json, pandas as pd\nfrom pathlib import Path\nregistros = json.loads(Path('docs/evidencias/experimentos-iniciais.json').read_text(encoding='utf-8'))\ndisplay(pd.DataFrame([dict(id=r['id'], algoritmo=r.get('algoritmo'), status=r['status'], run_id=r['run_id'], **r.get('resultado',{})) for r in registros]))")],
      "## 5.":[nbformat.v4.new_markdown_cell(report),nbformat.v4.new_code_cell("from IPython.display import display, Image\ndisplay(Image(filename='docs/evidencias/custo-por-threshold.png'))")],
      "## 6.":[nbformat.v4.new_markdown_cell(justificativa+"\n\n"+semana+"\n\n"+limites)],
      "## 7.":[nbformat.v4.new_markdown_cell("Pendente: candidato selecionado, ainda sem registro de versão ou promoção. Não executar a célula de entrega até concluir as seções 7–10.")],
      "## 9.":[nbformat.v4.new_markdown_cell("Pendente: implementar drift e relatório zero, justificar limites e arquivar referência na run selecionada.")]
    }
    cells=[]
    for cell in nb.cells:
        cells.append(cell)
        if cell.cell_type=="markdown":
            for prefix,addition in extras.items():
                if cell.source.startswith(prefix):cells.extend(addition)
    nb.cells=cells;nbformat.write(nb,"parte1.ipynb")
    import pandas as pd
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    dados=pd.read_csv("dados/transacoes_semanas_01_12.csv",dtype={"id_transacao":str,"id_cliente":str})
    rotulos=pd.read_csv("dados/rotulos_semanas_01_12.csv",dtype={"id_transacao":str})
    unido=dados.merge(rotulos,on="id_transacao",validate="one_to_one")
    conjuntos=[(mlflow.data.from_pandas(unido[unido.semana.between(1,10)],name="historico_semanas_01_10",targets="fraude"),"training"),(mlflow.data.from_pandas(unido[unido.semana.isin([11,12])],name="validacao_semanas_11_12",targets="fraude"),"validation")]
    for registro in completos:
        with mlflow.start_run(run_id=registro["run_id"]):
            for conjunto,contexto in conjuntos:mlflow.log_input(conjunto,context=contexto)
            for arquivo in ["docs/evidencias/auditoria-inicial.json","docs/evidencias/auditoria-temporal.json","docs/evidencias/ambiente.json"]:
                mlflow.log_artifact(arquivo,artifact_path="auditoria")
    with mlflow.start_run(run_id=vencedor["run_id"]):
        mlflow.set_tags({"decisao":"selecionado_por_custo_promocao_pendente","threshold_selecionado":str(m['threshold'])})
        for arq in ["docs/evidencias/experimentos-iniciais.json","docs/evidencias/comparacao-inicial.md","docs/evidencias/custo-por-threshold.png","docs/evidencias/tentativa-tecnica-inicial.json"]:
            mlflow.log_artifact(arq,artifact_path="referencia/experimentos")
        mlflow.log_artifacts("docs",artifact_path="referencia/documentacao")
    print(json.dumps({"selecionado":vencedor["id"],"run_id":vencedor["run_id"],"custo":m["custo"],"threshold":m["threshold"]}))


if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
