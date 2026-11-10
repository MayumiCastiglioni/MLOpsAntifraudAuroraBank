# 008 — Referência E03 preparada localmente

Data: 10/11/2026. Estado: preparação local concluída; anexação ao MLflow pendente.

## Decisão e evidência

O usuário pediu prosseguir com a referência do modelo. Reutilizamos o artefato persistido da run E03 e reprocessamos as semanas 11–12 sem retreino. O CSV local contém ID da transação, semana, 13 features, score, decisão no threshold 0,10 e rótulo. São 39.497 linhas; custos recalculados: semana 11 R$ 11.019,25 e semana 12 R$ 7.966,36. Hashes e métricas estão em `docs/evidencias/referencia-e03-preparada.json`; o gerador é `scripts/preparar_referencia_e03.py`.

## Limitação

O MLflow em localhost:5001 não responde; seu backend Postgres em localhost:5432 está indisponível e o Docker daemon não está ativo. Logo não foi possível anexar `referencia/` à run E03. Não apontamos a referência a outra run nem criamos tracking store concorrente, para preservar a linhagem e evitar apagar ou duplicar estado.

## Próximo passo

Quando o serviço original voltar, executar `mlflow.log_artifact` do CSV e manifesto na run `ff48c43154624ec9a1e3d16688909ef3`, sob `referencia/`, confirmar o caminho no catálogo e marcar etapa 3 concluída. Depois, a decisão de promover `champion` permanece separada e exige validação humana.
