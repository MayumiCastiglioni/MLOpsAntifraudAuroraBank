# Monitoramento — baseline, alertas e rótulos atrasados

A biblioteca em `monitoramento.py` produz relatórios de distribuição, alertas por magnitude, saída operacional e performance. Ela não decide incidente nem retreina o modelo.

## Como classifica as features

- **KS (estatística D e p-valor):** floats, score e inteiros ordinais `idade_conta_dias` e `qtd_transacoes_1h`.
- **Proporções e variação total:** categorias, booleanos, `hora_transacao` e `dia_semana`; inclui categorias novas e valores ausentes.
- **Saída operacional:** volume, quantidade/taxa bloqueada e valor bloqueado, sem depender de rótulos.
- **Performance:** custo, recall, precision e average precision globalmente e por canal, somente onde há rótulos explícitos. Custo final exige cobertura completa e fechamento explícito.

`monitorar(...)` retorna cinco tabelas: `continuas`, `categoricas`, `alertas`, `operacional` e `performance`. Cada linha da tabela `alertas` tem medida, valor, limite, indicador `alerta`, status e ação.

## Sem alerta versus dado indisponível

`sem_alerta` significa que a métrica pôde ser calculada e ficou abaixo do limite. `verificar_qualidade_dados` significa que não havia amostra válida suficiente para calcular a métrica em um ou ambos os lados. Nesse segundo caso `alerta` permanece falso, mas a ação pede conferir volume, conversão numérica, nulos e valores infinitos; não deve ser interpretada como distribuição estável.

Quando uma categoria não tem linhas em um dos lados, a tabela de drift e a tabela consolidada também registram `status=sem_amostra_valida` e `acao=verificar_qualidade_dados`. Quando há linhas com valor ausente, ausência é contabilizada como categoria própria.

## Política de alerta

Os limites padrão são KS D ≥ 0,10 e variação total ≥ 0,10, configuráveis na chamada. D=0,10 significa uma diferença máxima de 10 pontos percentuais entre CDFs; variação total=0,10 indica que é necessário redistribuir ao menos 10% da massa de probabilidade para igualar as distribuições. Os limites são heurísticos, ainda sem calibração histórica. `investigar` pede análise humana; não altera alias, modelo ou threshold.

## Relatório zero reproduzível

Execute `python scripts/gerar_relatorio_zero.py` na raiz. O script compara semana 11 (20.399 registros) com semana 12 (19.098) a partir da referência E03 e atualiza `docs/evidencias/relatorio-zero-semanas-11-12.json`. A referência tem 39.497 linhas, contrato v1.0, score, decisão e rótulo.

No baseline, `idade_conta_dias` apresenta KS D≈0,0594 e p≈1,13×10⁻³⁰. D fica abaixo do limite de magnitude, portanto não dispara investigação por drift. O p-valor pequeno, sozinho, não decide o alerta. A maior variação total categórica/discreta é `uf_cliente`, ≈0,0215. Nenhuma feature ultrapassa os limites no relatório zero.

## Testes e limites da evidência

A suíte automatizada atual tem 18 testes, incluindo consolidação da tabela de alertas, acionamento no limite inclusivo, encaminhamento de inteiros ordinais ao KS e tratamento de amostra indisponível. O resultado mais recente está em `docs/evidencias/testes-automatizados.json`.

Há somente uma comparação de referência para calibrar os limites. Seleção e corte usam semanas 11–12; são validação, não avaliação independente. Não presumir incidente ou retreino a partir de drift isolado.
