# 010 — Paridade da API com E03

Data: 10/11/2026. Estado: verificação concluída.

## Verificação

Enviamos cinco transações da semana 12 ao endpoint `POST /predict`, contendo somente as features na ordem do contrato v1.0. Comparamos cada resposta com a predição direta da versão registrada `antifraude` v1, origem na run `ff48c43154624ec9a1e3d16688909ef3`.

O endpoint `GET /api/modelo` também confirmou versão v1, contrato 1.0, threshold 0,10 e histórico da troca. Os cinco scores da API coincidiram com a predição do modelo após o arredondamento público para seis casas. A versão servida foi v1, o threshold foi 0,10 e todas as decisões `bloquear` coincidiram com a regra aplicada ao score original. A evidência com os resultados está em `docs/evidencias/paridade-api-e03.json`.

## Limites

Esta é uma checagem de integração em amostra de cinco registros, não uma avaliação independente de desempenho, disponibilidade ou comportamento sob carga.
