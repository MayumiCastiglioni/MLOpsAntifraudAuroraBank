# Arquitetura proposta

Estado em 10/11/2026: arquitetura implementada e verificada com comparação, monitoramento, referência, registry, alias champion e paridade da API. A promoção é a primeira versão do projeto (`antifraude` v1).

## Fluxo

Histórico → auditoria e junção 1:1 → divisão temporal → Pipeline por algoritmo → comparação de custo e threshold → registro de versão e referência no MLflow → alias champion → API → log de decisões → monitoramento sem e com rótulos.

## Responsabilidades

- Contrato YAML: fonte da ordem, tipos, categorias e semântica das 13 entradas.
- features.py: construção do pré-processamento, incluído no Pipeline; ajuste apenas no treino.
- Notebook: investigação, comparação, gráficos e justificativas; lógica reutilizável fica nos módulos.
- monitoramento.py: custo, drift, saída operacional, cobertura e performance global/segmentada.
- MLflow: runs, parâmetros, métricas, modelos, referências e promoção rastreável.
- FastAPI e frontend fornecidos: ingestão semanal, inferência, painel e decisões; avaliar comportamento antes de alterar.
- Postgres antifraude: transações, previsões, rótulos e histórico operacional. Backend MLflow separado logicamente.

## Organização futura

Scaffold original adaptado para a raiz com app/, contrato/, sql/, features.py, monitoramento.py e parte1.ipynb. Manter material/ intacto. Não criar abstrações ou serviços adicionais antes de necessidade comprovada.

## Política de avaliação

Escolher pelo custo com baselines no mesmo conjunto. Registrar custo por semana e sensibilidade do corte. Resultados das semanas 11–12 são validação usada na seleção, não teste independente. Não refazer treino com 11–12 sem nova decisão que preserve a avaliação exigida.

## Operação e limites

Separar disponibilidade, contrato, drift e performance. Monitorar entradas e scores antes dos rótulos; medir custo real apenas com cobertura informada. Não confundir repontuação com decisões originais. Preservar evidências por versão e semana.

Tratamento e decisões estão registrados nos ADRs 003–010. Alertas de magnitude solicitam investigação; a API carrega o alias champion e o threshold tagueado na versão.
