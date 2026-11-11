"""Auditoria local sem modificar dados ou executar a aplicação fornecida."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import yaml


def auditar(origem):
    with zipfile.ZipFile(origem) as z:
        prefixo = "antifraude_mlops/"
        bruto = z.read(prefixo + "dados/transacoes_semanas_01_12.csv")
        rotulos = z.read(prefixo + "dados/rotulos_semanas_01_12.csv")
        import io
        t = pd.read_csv(io.BytesIO(bruto), dtype={"id_transacao": str, "id_cliente": str})
        r = pd.read_csv(io.BytesIO(rotulos), dtype={"id_transacao": str})
        contrato = yaml.safe_load(z.read(prefixo + "contrato/contrato_features.yaml"))
    d = t.merge(r, on="id_transacao", validate="one_to_one", how="outer", indicator=True)
    violacoes = {}
    for f in contrato["features"]:
        col = f["nome"]
        if col not in t:
            violacoes[col] = {"ausente": True}
            continue
        s = t[col]
        erros = {"nulos": int(s.isna().sum())}
        if f["tipo"] == "categoria":
            erros["fora_categorias"] = int((~s.isin(f["valores"])).sum())
        else:
            n = pd.to_numeric(s, errors="coerce")
            erros["nao_finitos"] = int((~np.isfinite(n)).sum())
            if f["tipo"] in ("int", "bool"):
                erros["nao_inteiros"] = int((n.dropna() % 1 != 0).sum())
            if f["tipo"] == "bool":
                erros["fora_bool"] = int((~n.isin([0, 1])).sum())
            for limite, operador in [("min", lambda x,y:x<y), ("max", lambda x,y:x>y)]:
                if limite in f:
                    erros["fora_" + limite] = int(operador(n, f[limite]).sum())
        violacoes[col] = erros
    datas = pd.to_datetime(t.data_transacao, errors="coerce")
    esperado = t.valor_transacao / t.valor_medio_30d
    baselines = []
    for semana, g in d[d.semana.isin([11, 12])].groupby("semana"):
        bloqueia = (g.canal == "pix") & (g.valor_transacao > 1000)
        baselines.append({"semana": int(semana), "aprovar_tudo": round(float(g.loc[g.fraude == 1, "valor_transacao"].sum()),2), "regra_pix": round(float(g.loc[(g.fraude == 1) & ~bloqueia, "valor_transacao"].sum() + 15 * ((g.fraude == 0) & bloqueia).sum()),2)})
    return {"transacoes": len(t), "rotulos": len(r), "sha256_transacoes": hashlib.sha256(bruto).hexdigest(), "sha256_rotulos": hashlib.sha256(rotulos).hexdigest(), "ids_duplicados": {"transacoes": int(t.id_transacao.duplicated().sum()), "rotulos": int(r.id_transacao.duplicated().sum())}, "juncao": {str(k): int(v) for k,v in d["_merge"].value_counts().items()}, "contrato": violacoes, "datas_invalidas": int(datas.isna().sum()), "hora_divergente": int((datas.dt.hour != t.hora_transacao).sum()), "dia_semana_divergente": int((datas.dt.dayofweek != t.dia_semana).sum()), "razao_erro_maximo": float((esperado-t.razao_valor_media).abs().max()), "razao_fora_tolerancia": int((~np.isclose(esperado,t.razao_valor_media,atol=0.000051,rtol=0)).sum()), "tolerancia_razao": "absoluta 0.000051: arredondamento observado a quatro casas; verificar semântica além desta conferência", "rotulos_fora_binario": int((~r.fraude.isin([0,1])).sum()), "contestacao_ausente_por_classe": {str(k): int(v) for k,v in r.groupby("fraude").data_contestacao.apply(lambda s:s.isna().sum()).items()}, "semanas": d.groupby("semana").agg(n=("fraude","size"), fraudes=("fraude","sum"), taxa=("fraude","mean")).reset_index().to_dict(orient="records"), "baselines_validacao": baselines, "limites": "Auditoria preliminar; não prova ausência de vazamento upstream, disponibilidade histórica ou semântica correta de todas as features."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zip", type=Path)
    parser.add_argument("--saida", type=Path, default=Path("docs/evidencias/auditoria-inicial.json"))
    args = parser.parse_args()
    resultado = auditar(args.zip)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
