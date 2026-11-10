# Monitoramento — baseline e rótulos atrasados

A biblioteca em `monitoramento.py` produz relatórios de distribuição, alertas por magnitude, saída operacional e performance. Ela não decide incidente nem retreina o modelo.

## Como classifica as features

- **KS (estatística D e p-valor):** floats, score e inteiros ordinais `idade_conta_dias` e `qtd_transacoes_1h`. São medidas numéricas com ordem e distância interpretáveis.
- **Proporções e variação total:** categorias, booleanos, `hora_transacao` e `dia_semana`. Hora e dia da semana são distribuições cíclicas/discretas, não grandezas lineares. A função inclui categorias novas e ausentes.
- **Saída operacional:** volume, quantidade/taxa bloqueada e valor bloqueado, sem depender de rótulos.
- **Performance:** custo, recall, precision e average precision globalmente e por canal, apenas onde há rótulos explícitos. Ausência não vira classe zero; custo final exige cobertura completa e confirmação explícita de fechamento.

`monitorar(...)` devolve cinco tabelas: `continuas`, `categoricas`, `alertas`, `operacional` e `performance`. A tabela `alertas` mostra, por feature, medida, valor observado, limite e ação (`investigar` ou `sem_alerta`). Os limites padrão são KS D ≥ 0,10 e variação total ≥ 0,10, configuráveis na chamada. Um alerta é um pedido de análise humana; não altera alias, modelo ou threshold.

## Relatório zero reproduzível

Execute `python scripts/gerar_relatorio_zero.py` na raiz. O script compara semana 11 (20.399 registros) com semana 12 (19.098) a partir da referência E03 e atualiza `docs/evidencias/relatorio-zero-semanas-11-12.json`. A referência tem 39.497 linhas, contrato v1.0, score, decisão e rótulo.

No baseline, `idade_conta_dias` apresenta KS D≈0,0594 e p≈1,13×10⁻³⁰. A mudança acumulada é menor que o limite de magnitude, portanto não dispara investigação por esta política. Esse exemplo mostra por que o p-valor não decide sozinho: com amostras grandes uma diferença pode ser estatisticamente detectável sem ultrapassar o limite de magnitude escolhido. A maior variação total categórica/discreta é `uf_cliente`, ≈0,0215. Nenhuma feature ultrapassa os limites neste relatório zero.

## Interpretação dos limites

D=0,10 significa que a maior diferença entre as CDFs empíricas é de 10 pontos percentuais. Variação total=0,10 significa que é necessário redistribuir pelo menos 10% da massa de probabilidade para tornar as proporções iguais. São limites heurísticos interpretáveis, não uma taxa de falso alerta calibrada: existe apenas uma comparação de referência. Ao investigar, conferir qualidade do dado, tamanho da amostra, mudança de composição, impacto operacional e resultado após chegada dos rótulos. Não presumir incidente ou retreino. Recalibrar somente quando houver mais semanas operacionais.

## Verificações históricas

A suíte de 15 testes foi executada antes desta revisão semântica. Nesta revisão, o relatório zero foi recalculado pela função atual e o notebook integrado foi executado; a suíte não foi reexecutada. As limitações de vazamento upstream e seleção nas semanas 11–12 continuam explícitas.
