# Plano de implementação

1. **Auditoria dos dados:** verificar IDs únicos, junção 1:1 sem perdas, nulos, tipos, categorias, limites, regras semânticas, datas e distribuição semanal. Entrega: tabela de achados e decisões de tratamento.
2. **Ambiente isolado:** conferir Python, dependências e Postgres; preservar recursos do turnover. Integrar scaffold fora de material/. Entrega: instruções reproduzíveis e teste de conexões.
3. **Pipeline e comparação:** implementar features.py; treinar pelo menos dois algoritmos e registrar runs. Entrega: custo por semana, PR-AUC, precision, recall e três baselines.
4. **Escolha documentada:** comparar corte, estabilidade e economia. Entrega: justificativa de negócio e limitações da validação.
5. **Registro e inferência:** publicar versão com tags, descrição e referência; verificar cinco transações na API considerando arredondamento. Entrega: evidência de paridade.
6. **Monitoramento:** implementar funções reutilizáveis e relatório zero; justificar alertas e tratamento de rótulos incompletos. Entrega: tabelas globais e por segmento.
7. **Entrega:** atualizar changelog, salvar notebook e revisar conteúdo exportado. Entrega: ZIP sem avisos pendentes, com evidências verdadeiras.

Não há implementação de modelo autorizada por uma escolha implícita nesta documentação; algoritmo e corte dependem das análises.
