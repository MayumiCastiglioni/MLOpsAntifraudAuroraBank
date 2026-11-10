# 003 — Dados e ambiente da rodada inicial

Data: 06/11/2026. Estado: aceita para a execução inicial.

## Contexto e evidência

Auditorias inicial e temporal em docs/evidencias verificaram 240.384 pares transação/rótulo sem perdas e nenhuma violação nas verificações implementadas. data_contestacao é ausente nos legítimos, sem ausência de classe. Médias e outras features históricas não podem ser reconstruídas integralmente a partir do pacote.

## Decisão e alternativas

Preservar linhas e valores originais, sem imputação, remoção por data de contestação ou recálculo silencioso de features. Manter treino 1–10 e validação 11–12. Repetição de clientes entre períodos não altera essa regra e IDs não entram no Pipeline. Categorias vêm do contrato.

Usar MLflow 2.19.0 separado na porta 5001 e backend aurora_mlflow, preservando o servidor 3.16.0 existente na porta 5000. Aplicação na porta 8001, banco antifraude. Ambiente em caminho curto devido ao limite de caminhos do Windows; herda pacotes do Python local, com versões efetivas agora consolidadas em requirements.txt. A reprodução fixa as dependências Python, mas o MLflow e os serviços de produção continuam sendo componentes externos quando usados.

## Incidentes técnicos

A primeira instalação em .venv falhou por caminho longo. A primeira tentativa de experimento E01 falhou antes de treinar por artifact URI de Windows sem esquema file; a saída do MLflow também encontrou limitação de codificação do console. Preservada em tentativa-tecnica-inicial.json. Correção: experimento v2 com URI file explícita em diretório curto e saída UTF-8. Não interpretar essa falha como desempenho do algoritmo.

## Consequências

As verificações sustentam continuar a rodada inicial, mas não demonstram a ausência de vazamento upstream nem disponibilidade histórica de cada feature. Não há modelo promovido nesta etapa.
