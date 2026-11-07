# Monitoramento — etapa 1

Implementação concluída em 07/11/2026. Evidência: 15 testes passaram (sete anteriores e oito de monitoramento). Relatório zero e escolha de limites continuam pendentes.

## Interface

`monitorar(referencia, lote, contrato, threshold, segmento="canal", rotulos_fechados=False)` recebe DataFrames e devolve quatro tabelas. Os dados podem ser lidos diretamente do CSV exportado por `/api/semanas/{n}/dados.csv`. O lote precisa conter as features do contrato, score e valor_transacao. fraude é opcional; ausências não viram zero. O corte é explícito: o chamador deve garantir que referência e lote correspondem à mesma política/modelo ou registrar a comparação entre políticas.

- continuas: teste KS para floats e score, com estatística D, p-valor, tamanhos válidos e contagem de ausentes/não finitos. Sem amostra válida, o teste fica indisponível.
- categoricas: comparação de proporções para categorias, booleanas, hora e demais inteiros discretos. Inclui valores novos e ausentes, diferença em pontos percentuais e distância de variação total de 0 a 1. Não usa qui-quadrado, evitando pressupor frequências esperadas adequadas em categorias raras.
- operacional: volume, quantidade e taxa bloqueados, valor bloqueado e threshold. Usa todo o lote, sem precisar de rótulos.
- performance: resultados globais e por canal, com cobertura, custo observado, custo final, recall, precision e average precision. Sem fraudes, recall/AP são indefinidos; sem decisões positivas, precision é indefinida. Não apresentar zero como se fosse medida de desempenho válida nesses casos.

## Rótulos atrasados

Custo observado é calculado apenas nas linhas explicitamente rotuladas e não é extrapolado. Custo final só é preenchido com cobertura 100% e rotulos_fechados=True, que deve ser confirmado conforme a chegada dos rótulos. Cobertura completa sozinha não demonstra maturidade. Rótulos inválidos são rejeitados.

Scores e valores devem estar completos e válidos para operação/performance. O relatório KS informa valores inválidos nas features para que ausência não desapareça silenciosamente das estatísticas. Estas rotinas não substituem a validação completa do contrato.

## Verificação

`python -m unittest discover -s tests`

Casos novos: rótulo parcial sem imputação; fechamento explícito; ausência total de rótulos; operação sem rótulos e igualdade ao corte; categoria nova/ausente; KS sem mudança com ausência informada; segmento sem fraude; rótulo inválido.

Não houve comparação das semanas 11–12 nesta etapa, definição de alertas, retreino, promoção ou modificação do pacote de entrega anterior. Esses passos têm estados próprios.
