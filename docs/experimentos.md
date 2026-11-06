# Protocolo e registro de experimentos

Data: 06/11/2026. Protocolo definido antes do treino; nenhum resultado de modelo disponível.

## Por que ampliar

Comparar famílias com hipóteses diferentes, além do mínimo de dois algoritmos, para justificar a escolha por evidências. Quantidade não é objetivo: executar primeiro uma configuração por família, registrar inclusive falhas e descartes e evitar busca extensa na validação.

## Hipóteses iniciais

| ID | Família | Hipótese antes do teste | Limitação a observar |
|---|---|---|---|
| E01 | Regressão logística | Uma relação aditiva pode oferecer referência simples, rápida e interpretável | Pode perder interações; precisa de escala e codificação adequadas |
| E02 | Árvore de decisão com profundidade limitada | Regras não lineares simples podem reduzir custo e facilitar explicação | Instabilidade e probabilidades grosseiras em folhas pequenas |
| E03 | Random Forest | Agregar árvores pode capturar interações com menor variância que árvore única | Custo computacional e scores que exigem avaliação do corte |
| E04 | Extra Trees | Maior aleatoriedade nos cortes pode melhorar generalização e tempo comparada à floresta | Pode aumentar viés; não presumir superioridade |
| E05 | HistGradientBoostingClassifier | Boosting pode capturar relações não lineares complementares e corrigir erros sucessivos | Conferir codificação, categorias, memória e estabilidade; não assumir suporte automático |

A escolha destas famílias é uma decisão de protocolo; a vencedora continua aberta. Não adicionar bibliotecas externas (XGBoost, LightGBM, CatBoost) apenas para ampliar a lista. Sua inclusão futura exige hipótese distinta, compatibilidade e registro anterior à execução.

## Condições comparáveis

- Entrada sempre com as 13 features cruas, em Pipeline. Categorias e ordem derivadas do contrato.
- Treino 1–10; seleção 11–12, sem ajuste de transformações no período de validação. Semente 42 quando aplicável.
- Uma configuração inicial por família. Definir e registrar hiperparâmetros antes de executar. Sem pesos de classe, reamostragem ou calibração implícitos: qualquer variante é novo experimento com justificativa.
- Transformações podem diferir conforme algoritmo, mas devem estar registradas e ser compatíveis com produção. Comparar tempo de treino e inferência, além de resultado.
- Otimizar corte global em grade 0,01–0,99 com passo 0,01. Registrar regra de desempate antes da execução (proposta: menor taxa de bloqueio entre custos iguais).
- Métrica primária: soma dos valores de fraudes aprovadas + R$ 15 por legítima bloqueada. Identificar PR-AUC como average precision caso essa implementação seja adotada.
- Reportar total e semanas 11 e 12 separadas. Comparar aprovar tudo, regra Pix > R$ 1.000 e o mesmo modelo a 0,5.
- Resultados são validação usada na escolha; quanto mais tentativas, maior o risco de seleção otimista. Não chamar de teste independente. Variantes adicionais precisam de justificativa e orçamento explícito.

## Registro obrigatório de cada tentativa

Antes: ID, hipótese, família, configuração, pré-processamento, semente, período e versão do contrato. Depois: status (concluído/falhou/descartado), run_id, commit, duração, custo, corte, precision, recall, average precision, bloqueios legítimos, fraude monetária perdida e conclusão.

Registrar erros e descartes sem inventar métricas. Uma tentativa falha não equivale a evidência de baixa qualidade preditiva. Não apagar runs desfavoráveis. Diferenciar execução repetida por erro técnico de hipótese nova.

## Como isso entra na entrega

O professor recebe o notebook e o ZIP exportado, não necessariamente o repositório. Portanto:

1. Seção 4 do notebook: tabela de hipóteses ANTES dos resultados, configurações e run_ids de todas as tentativas.
2. Seção 5: resultados e baselines, curvas custo × corte e análise por semana.
3. Seção 6: comparação final, motivos de escolha/descarte, limitações e efeito da seleção na validação.
4. Cada tentativa tem sua run no MLflow. Arquivar também tabela consolidada e relatório de experimentos na run campeã, dentro de referencia/experimentos/, pois a célula original exporta essa pasta. Não confundir esses documentos com o dataset de referência.
5. Conferir o ZIP: a célula original não exporta automaticamente docs/ nem todas as runs. Incluir uma cópia dos documentos de decisões e pegadinhas em referencia/documentacao/ e um resumo suficiente das runs concorrentes antes de gerar a entrega.
6. Abrir o notebook salvo e inspecionar o ZIP final. Nenhuma hipótese deve aparecer só no GitHub e faltar na entrega.

## Registro atual

| ID | Status | Resultado / motivo |
|---|---|---|
| E01–E05 | Planejados | Aguardam auditoria completa, ambiente e configurações registradas |
