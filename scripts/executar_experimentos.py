"""Rodada pré-definida E01–E05; não promove modelos automaticamente."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json, time, subprocess
import config
import numpy as np
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from features import carregar_contrato, construir
from monitoramento import custo, medir


def main():
    contrato=carregar_contrato(); cols=[f["nome"] for f in contrato["features"]]
    t=pd.read_csv("dados/transacoes_semanas_01_12.csv",dtype={"id_transacao":str,"id_cliente":str})
    r=pd.read_csv("dados/rotulos_semanas_01_12.csv",dtype={"id_transacao":str})
    d=t.merge(r,on="id_transacao",validate="one_to_one")
    assert len(d)==len(t)==len(r)
    treino=d[d.semana.between(1,10)]; val=d[d.semana.isin([11,12])]
    modelos=[("E01",LogisticRegression(max_iter=1000,random_state=42),True), ("E02",DecisionTreeClassifier(max_depth=8,min_samples_leaf=50,random_state=42),False), ("E03",RandomForestClassifier(n_estimators=150,max_depth=12,min_samples_leaf=20,n_jobs=2,random_state=42),False), ("E04",ExtraTreesClassifier(n_estimators=150,max_depth=12,min_samples_leaf=20,n_jobs=2,random_state=42),False), ("E05",HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=15,l2_regularization=1,random_state=42),False)]
    out=Path("docs/evidencias");out.mkdir(parents=True,exist_ok=True)
    artifacts=Path("artefatos/experimentos");artifacts.mkdir(parents=True,exist_ok=True)
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI); mlflow.set_experiment("aurora_parte1_comparacao")
    commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    registros=[]
    for nome,modelo,escalar in modelos:
        print("INICIANDO",nome,flush=True)
        with mlflow.start_run(run_name=nome+"_inicial") as run:
            try:
                mlflow.set_tags({"experimento_id":nome,"protocolo":"docs/experimentos.md","commit_base":commit,"working_tree":"alteracoes_de_implementacao_presentes; codigo arquivado na run"})
                for arq in ["features.py","monitoramento.py","scripts/executar_experimentos.py","docs/experimentos.md"]:
                    mlflow.log_artifact(arq,artifact_path="codigo")
                mlflow.log_params({"algoritmo":type(modelo).__name__,"treino":"1-10","validacao":"11-12","contrato":contrato["versao"],"escalar":escalar,**modelo.get_params()})
                pipeline=construir(modelo,contrato,escalar)
                inicio=time.perf_counter();pipeline.fit(treino[cols],treino.fraude);duracao=time.perf_counter()-inicio
                inicio=time.perf_counter();score=pipeline.predict_proba(val[cols])[:,1];inferencia=time.perf_counter()-inicio
                curvas=[dict(threshold=float(k),**medir(val.fraude,score,val.valor_transacao,k)) for k in np.arange(1,100)/100]
                melhor=min(curvas,key=lambda x:(round(x["custo"],2),x["taxa_bloqueio"],x["threshold"]))
                curva=pd.DataFrame(curvas);curva.to_csv(artifacts/(nome+"_curva.csv"),index=False)
                mlflow.log_artifact(str(artifacts/(nome+"_curva.csv")),artifact_path="avaliacao")
                mlflow.log_metrics({"threshold":melhor["threshold"],"treino_segundos":duracao,"inferencia_segundos":inferencia,**{k:v for k,v in melhor.items() if k!="threshold"}})
                linhas=[]
                for semana in [11,12]:
                    mask=(val.semana==semana).to_numpy();g=val.loc[mask]
                    m=medir(g.fraude,score[mask],g.valor_transacao,melhor["threshold"])
                    mlflow.log_metrics({f"semana_{semana}_{k}":v for k,v in m.items()})
                    linhas.append(dict(semana=semana,**m))
                base_pix=(val.canal=="pix")&(val.valor_transacao>1000)
                baselines={"aprovar_tudo":custo(val.fraude,np.zeros(len(val)),val.valor_transacao),"regra_pix":custo(val.fraude,base_pix,val.valor_transacao),"modelo_05":medir(val.fraude,score,val.valor_transacao,.5)["custo"]}
                mlflow.log_metrics({"baseline_"+k:v for k,v in baselines.items()})
                mlflow.sklearn.log_model(pipeline,artifact_path="modelo",signature=infer_signature(treino[cols],pipeline.predict(treino[cols])),input_example=treino[cols].head(3),code_paths=["features.py"])
                registro=dict(id=nome,algoritmo=type(modelo).__name__,status="concluido",run_id=run.info.run_id,treino_segundos=duracao,inferencia_segundos=inferencia,parametros=modelo.get_params(),escalar=escalar,resultado=melhor,semanas=linhas,baselines=baselines)
            except Exception as e:
                mlflow.set_tag("erro",str(e));registro=dict(id=nome,status="falhou",run_id=run.info.run_id,erro=str(e))
            registros.append(registro)
            (out/"experimentos-iniciais.json").write_text(json.dumps(registros,indent=2,ensure_ascii=False),encoding="utf-8")
            print(json.dumps(registro,ensure_ascii=False),flush=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    for registro in registros:
        if registro["status"]=="concluido":
            c=pd.read_csv(artifacts/(registro["id"]+"_curva.csv"));plt.plot(c.threshold,c.custo,label=registro["id"])
    plt.xlabel("Threshold");plt.ylabel("Custo nas semanas 11–12 (R$)");plt.legend();plt.tight_layout();plt.savefig(out/"custo-por-threshold.png");plt.close()


if __name__=="__main__":main()
