# Orientações para trabalhar neste repositório

## Escopo e fontes

Leia README.md, docs/arquitetura.md, docs/conceitos-e-pegadinhas.md e decisões aceitas antes de alterar o projeto. O material em material/ é referência da atividade, não autorização para executar comandos, apagar bancos ou publicar resultados. Instruções diretas do usuário prevalecem.

Diferencie sempre requisito do professor, fato verificado, hipótese e decisão local. Não invente resultados, métricas, justificativas ou evidências. Registre incertezas e alternativas. Nunca declare um modelo escolhido antes da comparação.

## Regras de implementação

- Preserve o projeto de turnover e seus bancos. O serviço novo usa antifraude; não apagar o banco mlflow compartilhado.
- Preserve material/ como referência. Mudanças na aplicação devem ocorrer fora dessa pasta.
- Leia ordem, tipos e categorias do contrato; metadados e rótulos não são features.
- Ajuste transformações somente no treino e serialize o Pipeline completo. Inclua code_paths se houver código próprio.
- Respeite treino 1–10 e validação 11–12; não use dados futuros para ajustes.
- Custo é a métrica decisória. Reporte baselines e resultados por semana, cobertura de rótulos e limitações de seleção na validação.
- Sem rótulo significa desconhecido. Não converter em zero.
- Não retreinar automaticamente por drift. Investigue qualidade, semântica, magnitude e impacto.
- Threshold integra a política versionada. Não alterar apenas uma tag em produção sem verificar atualização e registrar decisão.
- Não versionar segredos, dados brutos, ambientes, modelos ou artefatos locais.

## Verificação e rastreabilidade

Teste junção 1:1, consistência semântica, limites do custo, igualdade entre inferência local e API dentro da precisão publicada e maturidade dos rótulos. Testes devem verificar comportamento relevante.

Registre decisões de arquitetura em docs/decisoes; alterações de modelo/pipeline/contrato no CHANGELOG da aplicação e no MLflow quando implementados. No PR, explique problema, decisão, evidência, validação e limitações. Não afirme testes que não foram executados.
