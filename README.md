# Banco Aurora · Antifraude MLOps

Construção e operação de um modelo antifraude para Pix, cartão presencial e cartão online, com decisões justificadas pelo custo de negócio.

**Status:** entrega técnica completa e empacotada. `antifraude@champion` aponta para Random Forest E03 v1, corte 0,10. O ZIP final está em `entrega_parte1_mayumi_castiglioni_<timestamp>.zip` e foi verificado sem avisos; resta anexá-lo à atividade escolar.

## Objetivo

Minimizar o valor das fraudes aprovadas mais R$ 15 por transação legítima bloqueada para verificação. Bloqueio não significa cancelamento. Acurácia não é o critério de escolha.

## Regras da prática

- Entrada: exatamente as 13 features cruas, na ordem do contrato.
- Treino: semanas 1–10. Validação: semanas 11–12, sem divisão aleatória.
- Comparar pelo menos dois algoritmos e escolher o threshold pelo custo na validação, entre 0,01 e 0,99.
- Comparar com aprovar tudo, bloquear Pix acima de R$ 1.000 e o próprio modelo com corte 0,5.
- Registrar Pipeline completo no MLflow como `antifraude`, com assinatura, exemplo e código necessário.
- Versão promovida: tags `threshold` e `motivo`, descrição e alias `champion`.
- Preparar monitoramento antes das semanas futuras; rótulos chegam uma semana depois.

Entrega informada no material: **11/11/2026 às 23h59**, horário de Brasília.

## Organização

- [Orientações para agentes](AGENTS.md)
- [Contexto e requisitos](docs/contexto-e-requisitos.md)
- [Arquitetura proposta](docs/arquitetura.md)
- [Conceitos e pegadinhas](docs/conceitos-e-pegadinhas.md)
- [Plano de implementação](docs/plano-de-implementacao.md)
- [Status e planejamento da entrega](docs/status-etapas.md)
- Notebook preenchido da atividade: `parte1.ipynb`
- Notebook executado de auditoria e comparação reproduzível: `notebooks/01_analise_e_escolha.ipynb`
- [Monitoramento implementado](docs/monitoramento.md)
- [Notebook reproduzível e pasta de entrega](docs/reproducao-e-entrega.md)
- [Resultados e justificativa da comparação](docs/evidencias/comparacao-inicial.md)
- [Protocolo de experimentos e evidências para entrega](docs/experimentos.md)
- [Decisões](docs/decisoes/README.md)
- [Contribuição e pull requests](CONTRIBUTING.md)
- `material/`: documentos e código originais do professor para consulta; não executar sem revisão.

## Como começar

A aplicação fornecida foi integrada na raiz, preservando material/. Use Python 3.11 e instale requirements.txt em ambiente próprio; requirements.local.txt registra as versões da execução local. No Windows, prefira caminho curto para o ambiente virtual.

1. Extraia os dois CSVs do ZIP para dados/ (ignorados no Git).
2. Configure .env a partir de .env.exemplo; use banco antifraude e um backend MLflow separado, sem apagar recursos existentes.
3. A execução atual usa MLflow em http://127.0.0.1:5001 e API em http://127.0.0.1:8001. Esses endereços devem constar no .env. O script scripts/servir_mlflow.py inicia o servidor usando a configuração local.
4. Inicie a API: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8001`.
5. Verifique custo e Pipeline: `python -m unittest discover -s tests`.
6. Reproduza a rodada: `python scripts/executar_experimentos.py`. Isso cria novas runs, não promove modelos. Preserve os relatórios anteriores antes de repetir.
7. Atualize documentação e notebook após cinco resultados concluídos: `python scripts/documentar_resultados.py`.

Não execute a opção de recomeçar do zero do material sobre bancos compartilhados.

Dados, credenciais, artefatos e modelos não são versionados. Os CSVs devem ser obtidos do ZIP original e permanecer locais. Os resultados de validação estão em docs/evidencias/ e não constituem teste independente.
