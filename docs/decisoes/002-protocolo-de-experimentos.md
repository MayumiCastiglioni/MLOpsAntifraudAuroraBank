# 002 — Protocolo de experimentos e entrega

Data: 06/11/2026. Estado: aceita para o protocolo; seleção de modelo permanece aberta.

## Contexto

O usuário pediu adiantar o máximo hoje, comparar diversos modelos e documentar as hipóteses iniciais e todas as tentativas na entrega.

## Alternativas e decisão

Comparar apenas duas famílias atende o mínimo, mas oferece menos contraste. Busca irrestrita aumenta custo e seleção otimista na validação. Adotar rodada limitada a cinco famílias complementares, uma configuração inicial cada, descritas em docs/experimentos.md antes do treino.

## Evidência e consequências

Solicitação explícita do usuário e critérios das seções 4–6 do notebook. Hipóteses, configurações, falhas e descartes integrarão notebook, MLflow e documentos exportados. A célula original não copia docs/ nem todas as runs: preparar resumos em referencia/ antes da exportação. Nenhum algoritmo ou threshold foi escolhido. Execução depende das verificações de dados e ambiente.
