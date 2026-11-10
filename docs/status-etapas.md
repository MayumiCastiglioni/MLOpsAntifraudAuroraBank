# Status e planejamento da entrega

Atualizado em 10/11/2026. **Conclusão técnica: 100% (10 de 10 blocos da entrega concluídos).** A pasta e o ZIP foram gerados e inspecionados sem avisos. A única ação restante está fora do repositório: anexar o ZIP na atividade da escola.

## Etapas

| Etapa | Status | Evidência ou resultado |
|---|---|---|
| 1. Implementar monitoramento | Concluída e verificada | `monitoramento.py`; 18/18 testes aprovados em 10/11; tratamento de rótulo atrasado e métricas globais/por canal; resultado em `docs/evidencias/testes-automatizados.json` |
| 2. Relatório zero e limites | Concluída | Comparação 11→12; política investigativa: KS D ≥ 0,10 ou variação total ≥ 0,10; sem retreino nem troca automática |
| 3. Referência | Concluída | 39.497 linhas, features, scores e rótulos anexados à run E03; SHA-256 conferido |
| 4. Registrar e promover | Concluída após aprovação humana | `antifraude` v1, `champion`, threshold 0,10, motivo e descrição |
| 5. Paridade da API | Concluída | Cinco previsões da semana 12 coincidem com o modelo na precisão publicada e nas decisões |
| 6. Notebook, changelog e pacote | Concluída | Notebook da atividade executado sem erros; changelog v1.0.0; ZIP íntegro, sem avisos, credenciais ou logs |

## Planejamento restante

Não há implementação pendente nesta entrega. Anexar `entrega_parte1_mayumi_castiglioni_<timestamp>.zip` à atividade até o prazo informado no material. Após a entrega, as próximas ações dependem de novas semanas: enviar lotes, registrar rótulos quando fecharem e investigar alertas. Não retreinar nem alterar o champion automaticamente.

O artefato local final está em pasta com nome `entrega/parte1_final_<timestamp>/`. O notebook exportado contém 15 células de código, todas executadas sem erro; espaços de resposta vazios foram removidos. Evidência: `docs/evidencias/notebook-atividade-executado.json`.

## Limitações mantidas explícitas

As semanas 11–12 foram usadas para seleção e não são um teste independente. A paridade da API é uma checagem de cinco transações, não um teste de carga. O limite de drift é provisório e tem apenas uma comparação de referência. O projeto não demonstra ausência de vazamento nas features históricas upstream nem garante desempenho futuro.
