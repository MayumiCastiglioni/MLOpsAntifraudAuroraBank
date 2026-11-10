# Reprodução e entrega integral

## Notebooks

- `parte1.ipynb`: respostas à atividade, consulta do modelo promovido, conferência da API e leitura do relatório zero. Em 10/11/2026, todas as células foram executadas sem erro no kernel Aurora MLOps (Python 3.11). O resultado da checagem de cinco previsões também está em `docs/evidencias/paridade-api-e03.json`.
- `notebooks/01_analise_e_escolha.ipynb`: análise reproduzível dos dados, auditoria do contrato, hipóteses registradas antes do treino, cinco famílias de modelo, varredura dos 99 cortes, baselines, métricas semanais e resumo da escolha. Para refazer os treinos, use `scripts/executar_notebook_analise.py` ou execute o notebook conforme as instruções do pacote.

## Gerar o pacote final

1. Configure `.env` a partir de `.env.exemplo`; mantenha os bancos de antifraude e MLflow separados e os serviços locais iniciados.
2. Execute `parte1.ipynb` até a célula final e salve o arquivo. A célula de checklist usa `--check-only` e não altera entregas anteriores.
3. Na raiz do projeto, execute `python scripts/preparar_entrega_final.py`. O script verifica o alias, tags, referência, API e dados locais; cria uma nova pasta com timestamp em `entrega/` e um novo ZIP na raiz. Não remove snapshots anteriores.
4. Confira `VERIFICACAO_ENTREGA.json` dentro da pasta gerada. Resolva qualquer aviso antes de anexar o ZIP à atividade.

O pacote inclui os dois notebooks, código, contrato, dados fornecidos, referência, artefato do modelo registrado, decisões e evidências. Não inclui `.env`, credenciais, bancos ou logs locais. A reprodução de treinos pode criar novas runs locais; não promove modelo automaticamente. A validação nas semanas 11–12 foi usada na escolha e não constitui avaliação independente.
