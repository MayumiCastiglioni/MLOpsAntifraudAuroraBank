# 007 — Relatório zero e limites de alerta

Data: 08/11/2026. Estado: relatório executado; política investigativa escolhida pelo usuário em 10/11/2026.

## Contexto e evidência

Com os CSVs locais e o artefato já registrado da run E03 (`ff48c43154624ec9a1e3d16688909ef3`), sem retreino, comparamos semana 11 (referência, 20.399 linhas) e semana 12 (19.098 linhas). A junção transações/rótulos validou 1:1. Os rótulos da validação estão completos. O relatório integral está em `docs/evidencias/relatorio-zero-semanas-11-12.json`.

No corte candidato 0,10, semana 12 teve 457 bloqueios (2,39% das transações), R$ 284.305,37 em valor bloqueado e custo final R$ 7.966,36, com recall 0,8385, precision 0,5339 e average precision 0,8161. Custos por canal: cartão online R$ 2.326,41; cartão presencial R$ 2.685,95; Pix R$ 2.954,00.

Entre os cinco testes KS para variáveis contínuas/score, nenhum p-valor foi pequeno (intervalo 0,313591–0,960372); para score, D=0,009664 e p=0,313591. Isso não prova igualdade. Com amostras grandes, diferenças pequenas podem reduzir p-valores sem relevância operacional; D e o impacto também precisam ser examinados. Para categorias/discretas, não calculamos p-valores: comparamos proporções pela variação total. A maior diferença foi idade_conta_dias (0,232567), seguida por uf_cliente (0,021484). O sinal motiva investigação, mas não explica causa nem prova impacto na performance.

## Opções para limites

1. **Sem alerta automático nesta implantação:** registrar o relatório como baseline e revisar semanalmente magnitudes e qualidade. Menor risco de falso alarme; pode atrasar resposta a mudança real.
2. **Alerta investigativo por magnitude:** sinalizar para análise humana KS D ≥ 0,10 em contínuas ou variação total ≥ 0,10 em categorias, sem retreino nem mudança de política. Limiares são provisórios e não calibrados com mais semanas; podem não capturar efeitos sutis e idade_conta_dias já os excederia.
3. **Calibrar com histórico mais longo:** adiar alertas até obter semanas operacionais adicionais e avaliar estabilidade por volume/canal. Evita tratar uma única comparação como distribuição de referência, mas deixa o período sem sinal automático.

## Decisão registrada

Em 10/11/2026, a usuária escolheu a opção 2: KS D ≥ 0,10 ou distância de variação total ≥ 0,10 gera investigação humana. O monitoramento não retreina nem muda o modelo automaticamente. Com os dados do relatório zero, `idade_conta_dias` acionaria investigação por magnitude; a mudança deve ser analisada, sem presumir incidente ou falha.

## Consequências e pendências

Os limites são provisórios: há somente uma comparação entre semanas, sem calibração histórica suficiente. Métrica da semana 12 é retrospectiva sobre validação usada na seleção, não garantia futura. Registrar estes limites como decisão operacional, sem alterar alias ou corte. Próxima etapa técnica: consolidar referência final de features/scores/rótulos na run E03, preservando rastreabilidade.

