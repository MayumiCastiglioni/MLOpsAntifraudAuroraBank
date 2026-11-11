# 006 — Monitoramento e rótulos atrasados

Data: 07/11/2026. Estado: implementação aceita e concluída; os limites foram decididos depois no registro 007.

## Contexto

O usuário solicitou executar uma etapa por vez. A etapa 1 exige drift, saída operacional e performance global/segmentada, respeitando rótulos atrasados.

## Decisão e alternativas

KS com D e p-valor para floats/score; comparação de proporções para categorias, booleanas, hora e contagens inteiras. Optamos por proporções e variação total em vez de qui-quadrado, pois reportam magnitude e não exigem frequências esperadas grandes para categorias raras. Valores novos e ausentes entram no alinhamento.

Medir custo apenas com rótulos conhecidos, identificado como observado/parcial. Exibir custo final somente com cobertura completa e fechamento explícito. Não extrapolar custo parcial e não imputar legítimo para rótulo ausente. Devolver métricas indefinidas como NaN quando faltam denominadores relevantes. Threshold deve ser informado e não é escolhido pelo monitoramento.

## Evidência e consequências

15 testes passaram, incluindo oito cenários novos em tests/test_monitoramento.py. Não definimos alertas nem comparamos semanas reais nesta etapa. Drift não dispara retreino. O relatório zero, promoção, paridade da API e pacote integral foram concluídos em etapas posteriores e têm evidências próprias.
