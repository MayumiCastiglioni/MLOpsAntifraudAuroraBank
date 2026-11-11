# 005 — Notebook integral da análise e snapshot de entrega

Data: 06/11/2026. Estado: aceita para a organização da análise; execução verificada nas evidências.

## Contexto

O usuário solicitou notebook explícito, executado e reproduzível, com resumo final na pasta de entrega. O notebook anterior consultava resultados já gerados e não retreinava os cinco modelos em suas células.

## Alternativas e decisão

Manter apenas tabelas salvas não demonstra o fluxo completo. Trocar o roteiro original inteiro confundiria etapas de análise e operação ainda pendentes. Criar notebook adicional que executa leitura, auditoria, pré-processamento, treino, thresholds, baselines, conferência do modelo e resumo. Preservar o roteiro amplo da atividade.

Criar snapshot local autossuficiente em entrega/, com módulos, contrato, CSVs originais, versões e evidências, sem .env ou segredos. A reprodução usa MLflow local temporário e não depende de API/Postgres nem promove candidatos.

## Consequências

Rodada repetida com as mesmas configurações para verificar reprodutibilidade; não é nova evidência de generalização. A comparação com custos e cortes originais deve passar, e o resumo é produzido das métricas calculadas. Código, notebook e documentação ficam no Git; dados e cópia local de entrega continuam ignorados. Na data deste registro, monitoramento, promoção e teste de API ainda estavam pendentes; foram concluídos em etapas posteriores (registros 007–010).
