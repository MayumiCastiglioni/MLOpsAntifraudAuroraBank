# Resumo final — escolha do candidato antifraude

**Escolha:** RandomForestClassifier (E03), com threshold global **0.10**. Bloquear para verificação quando score >= threshold.

## Por que escolhemos este modelo

Foi o menor custo observado entre cinco famílias e 99 cortes por família, nas mesmas semanas 11–12: **R$ 18.985,61** em duas semanas, média de **R$ 9.492,81 por semana**. A regra atual de Pix custou R$ 225.349,79; a economia observada foi **R$ 206.364,18 (91.58%)**. O próprio modelo a 0,5 custou R$ 99.338,94.

O candidato bloqueou 480 transações legítimas, com custo de atrito de R$ 7.200,00, e deixou passar R$ 11.785,61 em fraude. Recall: 83.17%; precision: 50.97%; average precision: 0.8130. As 480 transações legítimas bloqueadas afetaram 476 clientes distintos. `id_cliente` foi usado somente no relatório de impacto; não entrou nas features, e o custo de atrito continua sendo por transação.

## Alternativas e motivos de descarte

- E01 — LogisticRegression: custo R$ 37.608,05, corte 0.06; não selecionado nesta rodada por custo superior.
- E02 — DecisionTreeClassifier: custo R$ 32.578,35, corte 0.03; não selecionado nesta rodada por custo superior.
- E03 — RandomForestClassifier: custo R$ 18.985,61, corte 0.10; selecionado por menor custo.
- E04 — ExtraTreesClassifier: custo R$ 29.196,24, corte 0.06; não selecionado nesta rodada por custo superior.
- E05 — HistGradientBoostingClassifier: custo R$ 24.587,99, corte 0.06; não selecionado nesta rodada por custo superior.

A maior average precision foi de E05 (0.8320); ela mede ranking, não o prejuízo monetário. Por isso não substitui a função de custo.

## Consistência por semana

- Semana 11: custo R$ 11.019,25, 267 legítimas bloqueadas e R$ 7.014,25 em fraude aprovada.
- Semana 12: custo R$ 7.966,36, 213 legítimas bloqueadas e R$ 4.771,36 em fraude aprovada.

## O que foi documentado e reproduzido

Hipóteses iniciais, configurações, contrato, hashes dos dados, auditoria, divisão temporal, custo, baselines, curvas, métricas por semana, tempos e run_ids estão no notebook e nos arquivos de resultados. A falha técnica anterior E01 foi preservada separadamente; a reprodução usa as mesmas hipóteses e não apaga o histórico.

Execução UTC: 20261110T184047_082995Z. Run E03 criada nesta reprodução: `3d3afdd446784c8aa9a8a7737fe5ae50`. Esta run serve à reprodução e não é a origem da versão em produção. `antifraude@champion` v1 foi promovida da run original E03 `ff48c43154624ec9a1e3d16688909ef3`, conforme decisão aprovada; reproduzir não troca o alias.

## Limitações e próximos passos

As semanas 11–12 foram usadas para escolher modelo e corte: são validação de seleção, não teste independente. A redução observada não é garantia de economia futura. Não demonstramos a ausência de vazamento upstream nas médias e contagens históricas. A política de corte global simplifica custos que dependem do valor de cada transação. O monitoramento, referência, promoção/alias champion, paridade com a API e pacote integral estão concluídos e documentados no notebook de atividade `parte1.ipynb` e em `docs/status-etapas.md`. Este resumo registra a reprodução da análise, não é uma avaliação independente.


## Clientes legítimos impactados

No corte escolhido (0,10), 480 transações legítimas foram bloqueadas, afetando 476 clientes distintos nas semanas 11–12. Foram 266 clientes na semana 11 e 212 na semana 12; dois clientes aparecem em ambas. O custo de atrito continua calculado por transação (R$ 15 cada), conforme a demanda. `id_cliente` foi usado somente para deduplicar o relatório e não entrou nas features.
