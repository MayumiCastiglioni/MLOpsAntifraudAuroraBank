# Changelog — modelo antifraude

Uma entrada por versão que chegou (ou quase chegou) à produção, da mais nova para a mais antiga.
A versão aqui precisa bater com a descrição da versão no MLflow e, quando o contrato mudar, com o `contrato_features.yaml`.

Modelo de entrada:

```markdown
## vX.Y.Z — DD/MM/AAAA
- **Tipo:** modelo | pipeline | contrato
- **Versão no MLflow:** antifraude v<n>
- **O que mudou:**
- **Por quê:**
- **Evidência:** (run do MLflow, métrica, teste de drift)
- **Impacto:** (custo, taxa de bloqueio, recall — antes e depois)
- **Retreinou?** sim | não
```

---

<!-- Escreva a sua primeira entrada (v1.0.0) abaixo desta linha. -->

## v0.1.0 — 06/11/2026
- **Tipo:** pipeline
- **Versão no MLflow:** ainda sem versão de registry; runs E01–E05 em aurora_parte1_comparacao_v2.
- **O que mudou:** auditoria, aplicação integrada, custo, Pipeline e comparação de cinco famílias.
- **Por quê:** preparar decisão por custo com hipóteses e tentativas documentadas.
- **Evidência:** docs/evidencias/experimentos-iniciais.json e comparacao-inicial.md; run selecionada ff48c43154624ec9a1e3d16688909ef3.
- **Impacto:** candidato Random Forest a 0,10 custou R$ 18.985,61 em 11–12, contra R$ 225.349,79 da regra Pix. Nenhuma produção alterada.
- **Retreinou?** treinamento inicial de cinco famílias; promoção pendente. v1.0.0 será registrada quando os requisitos de produção forem cumpridos.
