# 007 — Relatório zero e limites de alerta

Data: 08/11/2026; recalculado em 10/11/2026 após correção semântica do drift. Estado: relatório e política investigativa concluídos.

## Contexto e evidência

Com os CSVs locais e o artefato já registrado da run E03 (`ff48c43154624ec9a1e3d16688909ef3`), sem retreino, comparamos semana 11 (referência, 20.399 linhas) e semana 12 (19.098 linhas). A junção transações/rótulos validou 1:1. Os rótulos da validação estão completos. O relatório integral está em `docs/evidencias/relatorio-zero-semanas-11-12.json`.

No corte candidato 0,10, semana 12 teve 457 bloqueios (2,39% das transações), R$ 284.305,37 em valor bloqueado e custo final R$ 7.966,36, com recall 0,8385, precision 0,5339 e average precision 0,8161. Custos por canal: cartão online R$ 2.326,41; cartão presencial R$ 2.685,95; Pix R$ 2.954,00.

O relatório zero foi recalculado com a natureza semântica das features. `idade_conta_dias` e `qtd_transacoes_1h` são ordinais numéricas e usam KS; hora e dia da semana, categorias e booleanos usam comparação de proporções. `idade_conta_dias` tem D=0,059378 e p≈1,13×10⁻³⁰. O p-valor é muito pequeno, mas D fica abaixo do limiar de magnitude 0,10 e não dispara investigação. Isso demonstra o efeito do tamanho amostral e por que p-valor isolado não decide. `qtd_transacoes_1h` tem D=0,003560; o score D=0,009664. A maior variação total entre categorias/discretas é `uf_cliente` (0,021484); hora=0,017850. Nenhuma feature aciona alerta no baseline após a classificação revisada. O relatório completo, incluindo sinalização explícita por feature, está em `docs/evidencias/relatorio-zero-semanas-11-12.json`.

## Opções para limites

1. **Sem alerta automático nesta implantação:** registrar o relatório como baseline e revisar semanalmente magnitudes e qualidade. Menor risco de falso alarme; pode atrasar resposta a mudança real.
2. **Alerta investigativo por magnitude:** sinalizar para análise humana KS D ≥ 0,10 em contínuas ou variação total ≥ 0,10 em categorias, sem retreino nem mudança de política. Limiares são provisórios e não calibrados com mais semanas; podem não capturar efeitos sutis. O baseline recalculado não tem feature acima dos limites.
3. **Calibrar com histórico mais longo:** adiar alertas até obter semanas operacionais adicionais e avaliar estabilidade por volume/canal. Evita tratar uma única comparação como distribuição de referência, mas deixa o período sem sinal automático.

## Decisão registrada

Em 10/11/2026, a usuária escolheu a opção 2: KS D ≥ 0,10 ou distância de variação total ≥ 0,10 gera investigação humana. O monitoramento não retreina nem muda o modelo automaticamente. Com a reclassificação semântica, nenhuma feature do relatório zero ultrapassa o limite; o p-valor diminuto de idade_conta_dias não basta para disparar alerta porque D=0,059378.

## Consequências e pendências

Os limites são provisórios: há somente uma comparação entre semanas, sem calibração histórica suficiente. Métrica da semana 12 é retrospectiva sobre validação usada na seleção, não garantia futura. Registrar estes limites como decisão operacional, sem alterar alias ou corte. Próxima etapa técnica: consolidar referência final de features/scores/rótulos na run E03, preservando rastreabilidade.

