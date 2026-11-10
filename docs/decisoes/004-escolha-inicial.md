# 004 — Escolha após rodada inicial

Data: 06/11/2026. Estado: aceita para selecionar candidato; promoção da mesma configuração foi aprovada e concluída em 10/11/2026 (registro 009).

Escolha para a próxima etapa: E03 (RandomForestClassifier), corte 0.10, pelo menor custo agregado observado. Custo total de R$ 18985.61 em duas semanas, média de R$ 9492.81/semana. Economia contra a regra Pix: R$ 206364.18 (91.58%). Legítimas bloqueadas: 480 transações (não clientes únicos). Fraude monetária aprovada: R$ 11785.61.

Alternativas: cinco famílias do protocolo. Evidência: docs/evidencias/experimentos-iniciais.json, curvas e runs listadas no relatório.

- Semana 11: custo R$ 11019.25; 267 legítimas bloqueadas; fraude perdida R$ 7014.25.
- Semana 12: custo R$ 7966.36; 213 legítimas bloqueadas; fraude perdida R$ 4771.36.

A seleção e o corte usam as mesmas semanas 11–12: não é teste independente nem garantia futura. A promoção posterior, aprovada pela usuária, está registrada em `009-promocao-e03.md`. O threshold global é uma simplificação exigida; o custo varia com o valor das transações.
