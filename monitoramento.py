"""Monitoramento reutilizável: qualidade, drift, operação e rótulos atrasados."""
import numpy as np
from sklearn.metrics import average_precision_score, precision_score, recall_score


def custo(real, bloquear, valores):
    y, b, v = np.asarray(real), np.asarray(bloquear), np.asarray(valores, dtype=float)
    if not (len(y) == len(b) == len(v)) or len(y) == 0:
        raise ValueError("Vetores devem ter mesmo tamanho não vazio")
    if not np.isin(y, [0, 1]).all() or not np.isin(b, [0, 1]).all() or not np.isfinite(v).all() or (v < 0).any():
        raise ValueError("Rótulos e decisões binários, valores finitos e não negativos são obrigatórios")
    b = b.astype(bool)
    return float(v[(y == 1) & ~b].sum() + 15 * ((y == 0) & b).sum())


def medir(real, score, valores, threshold):
    y, s, v = np.asarray(real), np.asarray(score), np.asarray(valores)
    if len(s) != len(y) or not np.isfinite(s).all() or ((s < 0) | (s > 1)).any() or not 0 <= threshold <= 1:
        raise ValueError("Scores e threshold devem ser finitos entre zero e um")
    b = s >= threshold
    return dict(custo=custo(y,b,v), recall=float(recall_score(y,b,zero_division=0)), precision=float(precision_score(y,b,zero_division=0)), average_precision=float(average_precision_score(y,s)), legitimas_bloqueadas=int(((y==0)&b).sum()), fraude_perdida=float(v[(y==1)&~b].sum()), taxa_bloqueio=float(b.mean()))


# Estas funções não escolhem limites de alerta nem retreinam modelos.
import pandas as pd
from scipy.stats import ks_2samp

# Estas variáveis inteiras têm ordem e distância com significado: dias de
# idade da conta e quantidade de transações. Hora e dia da semana são tratadas
# como distribuições cíclicas/discretas, não como magnitudes lineares.
COLUNAS_ORDINAIS_NUMERICAS = {"idade_conta_dias", "qtd_transacoes_1h"}


def _scores(df, coluna="score"):
    if df.empty:
        raise ValueError("Lote vazio")
    s = pd.to_numeric(df[coluna], errors="coerce").to_numpy(dtype=float)
    if not np.isfinite(s).all() or ((s < 0) | (s > 1)).any():
        raise ValueError("Scores devem estar completos e entre zero e um")
    return s


def drift_continuas(referencia, lote, colunas, limite_D=0.10):
    """KS com D/p-valor e sinal de investigação por magnitude.

    D é a maior diferença entre as distribuições acumuladas empíricas.
    O p-valor é contexto estatístico; o alerta usa D, não significância isolada.
    """
    linhas = []
    for coluna in colunas:
        ref = pd.to_numeric(referencia[coluna], errors="coerce").to_numpy(dtype=float)
        atual = pd.to_numeric(lote[coluna], errors="coerce").to_numpy(dtype=float)
        a, b = ref[np.isfinite(ref)], atual[np.isfinite(atual)]
        teste = ks_2samp(a, b) if len(a) and len(b) else None
        d = float(teste.statistic) if teste else np.nan
        linhas.append(dict(feature=coluna, n_referencia=len(a), n_lote=len(b),
                           invalidos_referencia=int((~np.isfinite(ref)).sum()),
                           invalidos_lote=int((~np.isfinite(atual)).sum()),
                           D=d,
                           p_valor=float(teste.pvalue) if teste else np.nan,
                           limite_alerta=float(limite_D),
                           alerta=bool(np.isfinite(d) and d >= limite_D),
                           acao="investigar" if np.isfinite(d) and d >= limite_D else "sem_alerta",
                           status="calculado" if teste else "sem_amostra_valida"))
    return pd.DataFrame(linhas)


def drift_categoricas(referencia, lote, colunas, limite_variacao_total=0.10):
    """Proporções alinhadas e distância de variação total (0–1).

    Inclui categorias novas e ausentes; não depende de aproximação qui-quadrado.
    A categoria nula usa chave própria, sem confundir ausência com texto literal.
    """
    linhas = []
    for coluna in colunas:
        def distribuicao(df):
            return df[coluna].map(lambda x: ("ausente", "") if pd.isna(x) else ("valor", str(x))).value_counts(normalize=True)
        a, b = distribuicao(referencia), distribuicao(lote)
        chaves = a.index.union(b.index)
        pa, pb = a.reindex(chaves, fill_value=0), b.reindex(chaves, fill_value=0)
        tv = float(np.abs(pa-pb).sum()/2) if len(referencia) and len(lote) else np.nan
        for chave in chaves:
            linhas.append(dict(feature=coluna, categoria=chave[1], ausente=chave[0]=="ausente",
                               proporcao_referencia=float(pa.at[chave]), proporcao_lote=float(pb.at[chave]),
                               diferenca_pp=float(100*(pb.at[chave]-pa.at[chave])),
                               variacao_total=tv, categoria_nova=chave not in a.index,
                               limite_alerta=float(limite_variacao_total),
                               alerta=bool(np.isfinite(tv) and tv >= limite_variacao_total),
                               acao="investigar" if np.isfinite(tv) and tv >= limite_variacao_total else "sem_alerta",
                               status="calculado" if np.isfinite(tv) else "sem_amostra"))
    return pd.DataFrame(linhas)


def saida_operacional(lote, threshold):
    """Mede a política informada; não infere o corte nem usa rótulos."""
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Threshold inválido")
    score = _scores(lote)
    valores = pd.to_numeric(lote.valor_transacao, errors="coerce").to_numpy(dtype=float)
    if not np.isfinite(valores).all() or (valores < 0).any():
        raise ValueError("Valores inválidos")
    bloqueio = score >= threshold
    return pd.DataFrame([dict(transacoes=len(lote), threshold=threshold,
                              bloqueadas=int(bloqueio.sum()), taxa_bloqueio=float(bloqueio.mean()),
                              valor_bloqueado=float(valores[bloqueio].sum()))])


def performance_rotulada(lote, threshold, segmento="canal", rotulos_fechados=False):
    """Custos observados são parciais até cobertura 100% E fechamento explícito.

    Só avalia linhas com classe explícita. Sem fraudes, recall e AP são
    indefinidos; sem bloqueios, precision é indefinida. Não imputar zero.
    """
    saida_operacional(lote, threshold)  # valida todos os scores e valores
    if "fraude" not in lote:
        lote = lote.assign(fraude=np.nan)
    presentes = lote.fraude.notna()
    if not lote.loc[presentes, "fraude"].isin([0, 1]).all():
        raise ValueError("Rótulos presentes devem ser binários")
    grupos = [("global", "todos", lote)]
    grupos += [(segmento, str(k), g) for k, g in lote.groupby(segmento, dropna=False)]
    linhas = []
    for escopo, grupo, df in grupos:
        conhecido = df[df.fraude.notna()]
        cobertura = len(conhecido)/len(df)
        completo = cobertura == 1 and bool(rotulos_fechados)
        linha = dict(escopo=escopo, segmento=grupo, transacoes=len(df), rotuladas=len(conhecido),
                     cobertura=cobertura, rotulos_fechados=bool(rotulos_fechados),
                     status="final" if completo else "parcial" if len(conhecido) else "sem_rotulos",
                     custo_observado=np.nan, custo_final=np.nan, recall=np.nan,
                     precision=np.nan, average_precision=np.nan, fraudes_observadas=0)
        if len(conhecido):
            y = conhecido.fraude.to_numpy(dtype=int)
            s = conhecido.score.to_numpy(dtype=float)
            bloqueio = s >= threshold
            c = custo(y, bloqueio, conhecido.valor_transacao)
            n_fraudes = int((y == 1).sum())
            linha.update(custo_observado=c, custo_final=c if completo else np.nan,
                         fraudes_observadas=n_fraudes,
                         recall=float(recall_score(y, bloqueio)) if n_fraudes else np.nan,
                         precision=float(precision_score(y, bloqueio, zero_division=0)) if bloqueio.any() else np.nan,
                         average_precision=float(average_precision_score(y,s)) if n_fraudes else np.nan)
        linhas.append(linha)
    return pd.DataFrame(linhas)


def monitorar(referencia, lote, contrato, threshold, segmento="canal", rotulos_fechados=False,
              limite_ks=0.10, limite_variacao_total=0.10):
    """Recebe tabelas (por exemplo, CSV exportado da API) e devolve relatórios.

    Floats, score e inteiros ordinais (`idade_conta_dias`,
    `qtd_transacoes_1h`) usam KS. Categorias, booleanas, hora e dia da semana
    usam proporções. ``alertas`` lista cada variável e a ação por magnitude;
    alerta pede investigação, não é veredito de incidente ou retreino.
    """
    if not 0 <= limite_ks <= 1 or not 0 <= limite_variacao_total <= 1:
        raise ValueError("Limites de drift devem estar entre zero e um")
    colunas_ks = [f["nome"] for f in contrato["features"]
                  if f["tipo"] == "float" or f["nome"] in COLUNAS_ORDINAIS_NUMERICAS]
    categoricas = [f["nome"] for f in contrato["features"]
                   if f["nome"] not in colunas_ks]
    continuas = drift_continuas(referencia, lote, colunas_ks + ["score"], limite_ks)
    distribuicoes = drift_categoricas(referencia, lote, categoricas, limite_variacao_total)
    alertas_ks = continuas.assign(tipo="ks", medida="D", valor=continuas["D"],
                                   limite=continuas["limite_alerta"])[
        ["feature", "tipo", "medida", "valor", "limite", "alerta", "acao"]]
    alertas_tv = distribuicoes.drop_duplicates("feature").assign(
        tipo="proporcoes", medida="variacao_total", valor=lambda d: d["variacao_total"],
        limite=lambda d: d["limite_alerta"])[
        ["feature", "tipo", "medida", "valor", "limite", "alerta", "acao"]]
    alertas = pd.concat([alertas_ks, alertas_tv], ignore_index=True)
    alertas["limite_ks"] = float(limite_ks)
    alertas["limite_variacao_total"] = float(limite_variacao_total)
    return dict(continuas=continuas,
                categoricas=distribuicoes,
                alertas=alertas,
                operacional=saida_operacional(lote,threshold),
                performance=performance_rotulada(lote,threshold,segmento,rotulos_fechados))
