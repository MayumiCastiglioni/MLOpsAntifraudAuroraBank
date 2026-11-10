# 009 — Registro e promoção da E03

Data: 10/11/2026. Estado: promovida após aprovação explícita da usuária.

## Decisão

A usuária aprovou registrar e mover `champion` para Random Forest E03, threshold 0,10. Criamos/confirmamos `antifraude` v1 a partir da run `ff48c43154624ec9a1e3d16688909ef3`, com tags `threshold=0.1`, `motivo` e `experimento_id=E03`, mais descrição do algoritmo e da evidência de custo.

## Verificação

Antes do alias, carregamos a versão pelo número, conferimos identidade do modelo e paridade das probabilidades para toda a semana 12 versus o artefato da run. Em seguida movemos `champion` e confirmamos versão, tags e run_id. Registro em `docs/evidencias/promocao-e03.json`.

## Limites

A seleção usa semanas 11–12, que não são teste independente. A promoção configura o Registry; a paridade do endpoint FastAPI é verificada na etapa seguinte. A troca não altera o threshold original do código: a aplicação lê o tag versionado.
