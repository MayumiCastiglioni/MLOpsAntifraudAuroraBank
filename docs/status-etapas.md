# Status das etapas restantes

Atualizado em 10/11/2026. Trabalho sequencial solicitado pelo usuário: concluir e reportar uma etapa antes da próxima.

| Etapa | Status | Evidência ou pendência |
|---|---|---|
| 1. Implementar monitoramento | Concluída e testada | monitoramento.py, tests/test_monitoramento.py; 15 testes passaram |
| 2. Relatório zero e limites de alerta | Concluída; política investigativa escolhida em 10/11 | KS D ≥ 0,10 ou variação total ≥ 0,10 gera investigação humana; sem retreino ou alteração automática. Limites provisórios, ancorados em uma única comparação |
| 3. Referência final do modelo | Concluída | CSV e manifesto anexados em `referencia/` à run E03 ff48c43154624ec9a1e3d16688909ef3; download confirmado pelo mesmo SHA-256 |
| 4. Registrar e promover | Pendente | Registry antifraude, tags, descrição e alias champion |
| 5. Paridade com API | Pendente | Conferir cinco transações e corte servido |
| 6. Entrega integral | Pendente | Completar notebook, changelog v1.0.0 e exportação final |

A análise e o notebook de seleção anteriores continuam concluídos. O pacote local anterior é uma entrega de análise, não a entrega integral da atividade. Os testes da etapa 1 usam exemplos controlados; não equivalem ao relatório zero nem à integração em produção.
