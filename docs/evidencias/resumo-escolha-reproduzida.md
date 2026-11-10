# Resumo final — escolha do candidato antifraude

**Escolha:** RandomForestClassifier (E03), com threshold global **0.10**. Bloquear para verificação quando score >= threshold.

## Por que escolhemos este modelo

Foi o menor custo observado entre cinco famílias e 99 cortes por família, nas mesmas semanas 11–12: **R$ 18.985,61** em duas semanas, média de **R$ 9.492,81 por semana**. A regra atual de Pix custou R$ 225.349,79; a economia observada foi **R$ 206.364,18 (91.58%)**. O próprio modelo a 0,5 custou R$ 99.338,94.

O candidato bloqueou 480 transações legítimas, com custo de atrito de R$ 7.200,00, e deixou passar R$ 11.785,61 em fraude. Recall: 83.17%; precision: 50.97%; average precision: 0.8130. Foram 480 transações legítimas bloqueadas, afetando 476 clientes distintos nas duas semanas (266 na semana 11 e 212 na semana 12; dois aparecem em ambas). O custo continua sendo por transação, como definido na demanda; `id_cliente` foi usado apenas para calcular pessoas distintas, sem entrar no modelo.

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

Execução UTC: 20261106T195635_167250Z. Run selecionada nesta reprodução: `eeca6c987d3143ed8835e3371db0ceed`.

## Limitações e próximos passos

As semanas 11–12 foram usadas para escolher modelo e corte: são validação de seleção, não teste independente. A redução observada não é garantia de economia futura. Não demonstramos a ausência de vazamento upstream nas médias e contagens históricas. A política de corte global simplifica custos que dependem do valor de cada transação. As etapas posteriores de monitoramento baseline, limites de alerta, referência, registro/alias champion, paridade com a API e pacote integral estão concluídas e têm evidências em `docs/status-etapas.md`. Este arquivo permanece restrito ao resumo da análise e escolha do candidato.


## Clientes legítimos impactados

No threshold 0,10, 480 transações legítimas foram bloqueadas, afetando 476 clientes distintos nas semanas 11–12. O recorte por semana identifica 266 clientes na semana 11 e 212 na semana 12; dois aparecem em ambas. O custo de atrito é calculado por transação (R$ 15), e `id_cliente` não é feature.
