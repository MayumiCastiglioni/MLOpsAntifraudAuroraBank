# Conceitos e pegadinhas

Este inventário resulta de leitura estática do pacote; hipóteses sobre dados precisam de medição.

| Tema | Risco | Conduta |
|---|---|---|
| Acurácia | Aprovar tudo já acerta aproximadamente 98,5% segundo a demanda | Escolher por custo e mostrar baselines |
| PR-AUC | Bom ranking não garante menor prejuízo | Usar como apoio; definir precisamente a implementação da métrica |
| Custo | Contagem de fraudes ignora seus valores | Somar valor dos falsos negativos e R$ 15 por falso positivo |
| Threshold | 0,5 não representa os custos | Varrer 0,01–0,99 e avaliar sensibilidade e cada semana |
| Threshold global | Prejuízo varia por transação | Cumprir política pedida e explicitar sua simplificação |
| Temporalidade | Divisão aleatória mistura períodos | Respeitar semanas 1–10 e 11–12 |
| Seleção | Validação escolhe modelo e corte | Não apresentar como teste independente |
| Pipeline | Transformações diferentes em produção | Serializar pré-processamento e código próprio |
| Categorias | Inferir lista só do treino perde categorias válidas | Derivar listas do contrato |
| Metadados | IDs, semana e datas viram atalhos | Não entram nas 13 features |
| Rótulos | Ausente tratado como legítimo | Manter desconhecido e informar maturidade/cobertura |
| Drift | P-valor pequeno vira incidente automático | Considerar D, tamanho amostral, magnitude e impacto; justificar alertas |
| Semântica | razao_valor_media não é conferida pela regra YAML atual | Auditar valor_transacao / valor_medio_30d com tolerância documentada |
| Histórico | Validador de upload exige uma semana | Validar por semana e acrescentar verificações gerais |
| API | Score é arredondado a seis casas em /predict | Comparar com precisão compatível; decisão usa score original |
| Cache | Tag threshold muda sem mudar versão e não recarrega | Versionar política e verificar o corte efetivamente servido |
| Painel | Alguns rótulos já produzem custo parcial | Exibir cobertura e não comparar como semana encerrada |
| Repontuar | Painel usa a previsão mais recente | Preservar avaliação original antes de repontuar |
| Entrega | Célula remove e recria entrega/ | Não manter trabalho manual nessa pasta |
| Infraestrutura | README sugere apagar mlflow ao recomeçar | Não executar sobre banco compartilhado com turnover |

## Critério de decisão

Para cada problema: registrar observação → hipóteses → evidência necessária → alternativas → decisão → consequência e forma de verificar. Drift isolado não autoriza concluir perda de desempenho nem necessidade de retreino.
