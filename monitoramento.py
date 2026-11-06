"""Custo de negócio e métricas reutilizáveis. Drift será implementado na etapa 6."""
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
