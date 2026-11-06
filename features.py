"""Pipeline de entrada crua; categorias definidas pelo contrato."""
from pathlib import Path
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline


def carregar_contrato():
    return yaml.safe_load((Path(__file__).resolve().parent / "contrato/contrato_features.yaml").read_text(encoding="utf-8"))


def construir(modelo, contrato, escalar=False):
    categorias = [f for f in contrato["features"] if f["tipo"] == "categoria"]
    numericas = [f["nome"] for f in contrato["features"] if f["tipo"] != "categoria"]
    transformador = ColumnTransformer([
        ("numericas", StandardScaler() if escalar else "passthrough", numericas),
        ("categoricas", OneHotEncoder(categories=[f["valores"] for f in categorias], handle_unknown="error", sparse_output=False), [f["nome"] for f in categorias]),
    ], remainder="drop")
    return Pipeline([("preprocessamento", transformador), ("classificador", modelo)])
