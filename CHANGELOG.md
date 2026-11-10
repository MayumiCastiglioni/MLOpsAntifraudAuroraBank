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

<!-- Entrada v1.0.0 registrada em 10/11/2026. -->

## v1.0.0 — 10/11/2026
- **Tipo:** modelo, pipeline e monitoramento
- **Versão no MLflow:** `antifraude` v1; alias `champion`; run `ff48c43154624ec9a1e3d16688909ef3`.
- **O que mudou:** Random Forest E03 com Pipeline do contrato v1.0, threshold 0,10, tags `threshold` e `motivo`, descrição e referência das semanas 11–12 anexada à run. Monitoramento inclui drift, saída operacional e performance com rótulos atrasados. A API foi conferida contra cinco previsões diretas do modelo.
- **Por quê:** menor custo observado entre cinco famílias e 99 cortes avaliados nas semanas 11–12; integra a versão rastreável com o serviço e prepara a investigação semanal de mudanças.
- **Evidência:** `docs/evidencias/promocao-e03.json`, `docs/evidencias/paridade-api-e03.json`, `docs/evidencias/relatorio-zero-semanas-11-12.json`; referência arquivada na run de origem.
- **Impacto:** validação de seleção: R$ 18.985,61 nas duas semanas (média R$ 9.492,81/semana), contra R$ 225.349,79 da regra Pix > R$ 1.000; 480 transações legítimas bloqueadas e R$ 11.785,61 em fraudes aprovadas. Não é teste independente nem garantia de economia futura. Alertas por magnitude solicitam investigação; não retreinam nem alteram o modelo.
- **Retreinou?** treino inicial E03 ocorreu na comparação; a promoção não retreinou. Nenhum retreino automático.

<!-- Escreva a sua primeira entrada (v1.0.0) abaixo desta linha. -->

## v0.1.0 — 06/11/2026
- **Tipo:** pipeline
- **Versão no MLflow:** ainda sem versão de registry; runs E01–E05 em aurora_parte1_comparacao_v2.
- **O que mudou:** auditoria, aplicação integrada, custo, Pipeline e comparação de cinco famílias.
- **Por quê:** preparar decisão por custo com hipóteses e tentativas documentadas.
- **Evidência:** docs/evidencias/experimentos-iniciais.json e comparacao-inicial.md; run selecionada ff48c43154624ec9a1e3d16688909ef3.
- **Impacto:** candidato Random Forest a 0,10 custou R$ 18.985,61 em 11–12, contra R$ 225.349,79 da regra Pix. Nenhuma produção alterada.
- **Retreinou?** treinamento inicial de cinco famílias; promoção pendente. v1.0.0 será registrada quando os requisitos de produção forem cumpridos.
