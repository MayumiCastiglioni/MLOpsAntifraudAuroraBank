# Banco Aurora · Antifraude MLOps

Construção e operação de um modelo antifraude para Pix, cartão presencial e cartão online, com decisões justificadas pelo custo de negócio.

**Status:** fundação documental. Nenhum modelo foi treinado, escolhido ou promovido neste repositório.

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
- [Decisões](docs/decisoes/README.md)
- [Contribuição e pull requests](CONTRIBUTING.md)
- `material/`: documentos e código originais do professor para consulta; não executar sem revisão.

## Como começar

Leia os documentos acima antes de implementar. A aplicação ainda não foi instalada ou integrada. As instruções originais estão em `material/antifraude_mlops/README.md`; seus comandos devem ser revisados conforme o ambiente local. Não executar a opção de recomeçar do zero em bancos compartilhados.

Dados, credenciais, artefatos e modelos não são versionados. Os CSVs devem ser obtidos do ZIP original e permanecer locais. Não há resultados de performance disponíveis nesta etapa.
