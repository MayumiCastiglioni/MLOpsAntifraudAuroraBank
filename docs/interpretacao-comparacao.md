# Interpretação e sensibilidade

O boosting E05 teve maior average precision (0,8320 versus 0,8130), mas custo maior (R$ 24.587,99 versus R$ 18.985,61). Seu valor de fraude aprovada foi R$ 17.597,99, contra R$ 11.785,61 da floresta; apesar de bloquear 14 legítimas a menos, essa economia de R$ 210 não compensou a perda monetária adicional. Não escolher pela métrica de ranking isolada.

A Random Forest também teve custo inferior aos demais em cada uma das semanas, sem depender de compensar um resultado ruim em uma semana pelo outro. Isso é evidência observada, não teste estatístico de superioridade futura.

Cortes próximos do selecionado, sem novas configurações treinadas:

|   threshold |   custo |   recall |   precision |   average_precision |   legitimas_bloqueadas |   fraude_perdida |   taxa_bloqueio |
|------------:|--------:|---------:|------------:|--------------------:|-----------------------:|-----------------:|----------------:|
|        0.07 | 21639.8 | 0.858333 |    0.397377 |            0.813039 |                    781 |          9924.75 |       0.0328126 |
|        0.08 | 20316.6 | 0.845    |    0.437446 |            0.813039 |                    652 |         10536.6  |       0.029344  |
|        0.09 | 19604.9 | 0.835    |    0.482659 |            0.813039 |                    537 |         11549.9  |       0.0262805 |
|        0.1  | 18985.6 | 0.831667 |    0.509704 |            0.813039 |                    480 |         11785.6  |       0.0247867 |
|        0.11 | 21875.7 | 0.821667 |    0.530108 |            0.813039 |                    437 |         15320.7  |       0.0235461 |
|        0.12 | 24794.9 | 0.811667 |    0.558486 |            0.813039 |                    385 |         19019.9  |       0.0220776 |
|        0.13 | 24239.9 | 0.811667 |    0.583234 |            0.813039 |                    348 |         19019.9  |       0.0211408 |
