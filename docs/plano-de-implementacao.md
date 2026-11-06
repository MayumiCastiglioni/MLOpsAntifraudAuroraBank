# Plano de execução — Parte 1

Atualizado em 06/11/2026. Entrega exigida: 11/11/2026, às 23h59 (Brasília).
Estado: execução em 06/11; auditorias e ambiente preparados, Pipeline e custo implementados; comparação inicial em andamento. Evidências em docs/evidencias/.
Datas abaixo são metas propostas, não resultados ou compromissos já cumpridos.

## Prioridade atual: adiantar em 06/11

O usuário solicitou concentrar o máximo de avanço hoje. As datas da tabela abaixo são reserva de prazo, não impedimento para antecipar etapas. Ordem do dia: auditoria reproduzível → ambiente e scaffold → custo e Pipeline → rodada inicial das cinco famílias → monitoramento → integração, conforme as verificações permitirem. Nenhuma etapa deve ser declarada concluída sem evidência.

Todo teste deve seguir [o protocolo de experimentos](experimentos.md), aparecer no notebook e acompanhar a exportação final, inclusive tentativas descartadas ou malsucedidas. O escopo da rodada inicial é cinco configurações, uma por família, sem busca extensa.

## Estratégia

Primeiro verificar dados e ambiente; depois comparar modelos e políticas de corte; por último promover e reunir evidências. A decisão será pelo custo, preservando o contrato e a avaliação temporal. Não ampliar a infraestrutura antes de necessidade comprovada.

## Etapas e critérios de conclusão

| Etapa / meta | Trabalho | Entrega e condição para avançar | Notebook |
|---|---|---|---|
| 1 — 06–07/11 | Auditar ZIP e CSVs: IDs, junção 1:1, cobertura, nulos, tipos, categorias, limites, datas e razão valor/média. Conferir Python e dependências em ambiente próprio | Relatório de achados, contagens antes/depois da junção e questões semânticas resolvidas ou explicitadas; sem correção silenciosa | 0–1 |
| 2 — 07/11 | Integrar scaffold fora de material/, configurar Postgres e MLflow sem interferir no turnover, separar semanas 1–10 e 11–12 | Conexões verificadas; contrato e conjuntos documentados; resposta sobre divisão temporal | 0–2 |
| 3 — 08/11 | Implementar custo reutilizável em monitoramento.py e pré-processamento em features.py; derivar ordem e categorias do contrato | Testes do custo com casos conhecidos; Pipeline recebe somente 13 features cruas, aprende transformações apenas em 1–10 e pode ser serializado | 3 e 5 |
| 4 — 08–09/11 | Treinar pelo menos dois algoritmos, cada um em sua run; varrer cortes 0,01–0,99 em 11–12 | Tabela e gráfico de custo por corte; custo agregado e por semana, PR-AUC, recall, precision, falsos positivos e valor das fraudes aprovadas; três baselines no mesmo conjunto | 4–5 |
| 5 — 09/11 | Escolher modelo e corte com evidências, estabilidade entre semanas e sensibilidade a cortes próximos | Justificativa para o negócio: custo semanal, economia, clientes legítimos afetados e fraude restante. Se o piso não for atingido, investigar e registrar; não promover declarando aprovação | 6 |
| 6 — 09–10/11 | Completar monitoramento e relatório zero 11 versus 12; definir referência com features, score e rótulo | Funções de drift, taxa/valor bloqueados, cobertura e performance global/por segmento; limites justificados sem depender só de p-valor | 9 |
| 7 — 10/11 | Registrar versão escolhida, referência e código; definir threshold/motivo e descrição antes de mover champion; verificar API | Referência em referencia/ na run campeã; cinco transações da semana 12 com paridade compatível com arredondamento da API e decisões iguais; corte efetivo conferido | 7–8 |
| 8 — 11/11 | Revisar notebook, changelog e evidências; gerar e inspecionar entrega | Notebook salvo e textos completos; v1.0.0 coerente com MLflow; ZIP com arquivos esperados e avisos resolvidos. Reservar tempo antes de 23h59 | 10 |

## Experimentos iniciais propostos

Proposta inicial ampliada no protocolo de experimentos: regressão logística, árvore de decisão, Random Forest, Extra Trees e HistGradientBoosting. A comparação original entre regressão logística e Random Forest permanece como referência de contraste: uma referência simples e um modelo capaz de representar relações não lineares. A dupla é proposta, não escolha definitiva. Validar suporte ao Pipeline, predict_proba e ambiente antes de adotar. Começar com poucos hiperparâmetros, sem busca extensa na validação.

Definir precisamente PR-AUC (por exemplo, average precision, explicitamente identificada) para evitar comparar implementações diferentes. Não confundir ROC-AUC com a métrica solicitada.

## Decisões a registrar

| Decisão | Evidência necessária | Situação |
|---|---|---|
| Tratamento de dados inconsistentes | Frequência, exemplos, regra do contrato e efeito do tratamento | Aberta |
| Pré-processamento e algoritmos | Compatibilidade com contrato, características dos dados e comparação inicial | Proposta |
| Modelo e threshold | Custo contra aprovar tudo, Pix > R$ 1.000 e mesmo modelo a 0,5; análise por semana | Aberta |
| Segmento de monitoramento | Volume e relevância operacional; canal é candidato inicial | Aberta |
| Limites de alerta | Relatório zero, magnitude, volume e relevância prática | Aberta |
| Promoção | Piso atendido, rastreabilidade e inferência verificada | Pendente |

Cada registro deve conter contexto, alternativas, evidência, escolha, consequências e limitações. Hipótese não vira decisão aceita sem análise.

## Verificações críticas

- A junção deve preservar cada transação uma única vez. Ler IDs como texto.
- O validador de upload aceita uma semana por arquivo; o histórico exige validação por semana e conferências gerais.
- Confirmar regras semânticas mesmo quando o YAML não as verifica.
- Metadados e rótulos ficam fora das features. Não ajustar transformações com semanas 11–12.
- Modelos e baselines usam as mesmas linhas e definição de custo. Na regra atual, acima de R$ 1.000 significa > 1.000, apenas Pix.
- O threshold exigido é global. Sua otimização usa 11–12, portanto resultados são validação de seleção, não teste independente.
- Ausência de rótulo não é classe zero. Informar cobertura e maturidade; não declarar custo final com rótulos parciais.
- Registrar a versão antes de promover e conferir o corte servido: editar só a tag de uma versão carregada pode não atualizar o cache.
- Scores em /predict têm seis casas decimais; verificar precisão compatível e decisão sobre score original.
- Preservar evidências antes de repontuar; o painel usa as previsões mais recentes.
- A célula de entrega recria entrega/. Não guardar trabalho manual ali nem executar comandos de apagar bancos compartilhados.

## Organização do trabalho

Usar branches codex/<assunto> e PRs por etapa coerente: dados e ambiente; pipeline e comparação; monitoramento; produção e entrega. Cada PR explica decisão, evidências, verificações e limitações. Documentação não implica que uma etapa foi executada.

## Próxima ação concreta

Auditar os dois CSVs diretamente do ZIP ou de uma pasta local ignorada pelo Git. Produzir relatório de contagens e inconsistências antes de limpar dados, treinar ou escolher modelo. Em paralelo lógico, conferir a compatibilidade do ambiente, sem alterar serviços existentes.

## Situação ao final da rodada de 06/11

1. Auditoria inicial e temporal executadas; limitações upstream explicitadas no registro 003.
2. Scaffold integrado e conexões verificadas; seis tabelas no banco antifraude, MLflow 2.19.0 separado em 5001 e API em 8001.
3. Pipeline e custo implementados; sete testes passaram.
4. Cinco modelos concluídos em runs distintas, com curvas, baselines, configuração, métricas por semana e dados de lineage. Uma tentativa técnica anterior falhou antes do treino e está preservada.
5. Candidato selecionado: Random Forest, corte 0,10; justificativa em comparacao-inicial.md e registro 004. Custo de R$ 18.985,61 nas duas semanas. Sem promoção.

Próximas etapas: monitoramento baseline e relatório zero; referência final, registro da versão, paridade de API e empacotamento da entrega.
