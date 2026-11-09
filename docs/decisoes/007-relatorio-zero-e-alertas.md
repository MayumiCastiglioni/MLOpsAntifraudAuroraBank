# 007 — Relatório zero e limites de alerta

Data: 08/11/2026. Estado: relatório executado; decisão operacional de limites pendente.

## Contexto e evidência

Com os CSVs locais e o artefato já registrado da run E03 (`ff48c43154624ec9a1e3d16688909ef3`), sem retreino, comparamos semana 11 (referência, 20.399 linhas) e semana 12 (19.098 linhas). A junção transações/rótulos validou 1:1. Os rótulos da validação estão completos. O relatório integral está em `docs/evidencias/relatorio-zero-semanas-11-12.json`.

No corte candidato 0,10, semana 12 teve 457 bloqueios (2,39% das transações), R$ 284.305,37 em valor bloqueado e custo final R$ 7.966,36, com recall 0,8385, precision 0,5339 e average precision 0,8161. Custos por canal: cartão online R$ 2.326,41; cartão presencial R$ 2.685,95; Pix R$ 2.954,00.

Entre variáveis contínuas, o maior KS foi score (D=0,009664; p=0,313591). A maior mudança categórica/discreta foi idade_conta_dias (variação total=0,232567); próxima foi uf_cliente (0,021484). Isso sugere investigar mudança de composição de idade das contas, mas não explica causa nem prova impacto na performance. P-valor não deve ser usado sozinho para alerta.

## Opções para limites

1. **Sem alerta automático nesta implantação:** registrar o relatório como baseline e revisar semanalmente magnitudes e qualidade. Menor risco de falso alarme; pode atrasar resposta a mudança real.
2. **Alerta investigativo por magnitude:** sinalizar para análise humana KS D ≥ 0,10 em contínuas ou variação total ≥ 0,10 em categorias, sem retreino nem mudança de política. Limiares são provisórios e não calibrados com mais semanas; podem não capturar efeitos sutis e idade_conta_dias já os excederia.
3. **Calibrar com histórico mais longo:** adiar alertas até obter semanas operacionais adicionais e avaliar estabilidade por volume/canal. Evita tratar uma única comparação como distribuição de referência, mas deixa o período sem sinal automático.

## Pendências e consequências

É necessária decisão humana sobre qual opção usar e eventual ajuste de limites, inclusive aceitação de alerta investigativo para idade_conta_dias. Nenhum alerta operacional foi ativado, nenhum modelo foi retreinado e nenhum alias/corte foi alterado. A métrica da semana 12 é avaliação retrospectiva sobre validação usada na seleção, não garantia futura. Próxima etapa técnica independente: consolidar referência final features/scores/rótulos na run E03; depende de confirmar a destinação e retenção do artefato de referência.
