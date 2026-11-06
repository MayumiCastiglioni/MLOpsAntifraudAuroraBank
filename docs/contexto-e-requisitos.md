# Contexto e requisitos

Fonte: demanda_parte1.md e parte1.ipynb em material/antifraude_mlops/. Cenário acadêmico: Banco Aurora.

## Requisitos do professor

13 features conforme contrato; junção de transações e rótulos 1:1 sem perda; treino temporal 1–10 e validação 11–12; pelo menos dois algoritmos; métricas PR-AUC, recall, precision e custo; corte escolhido na validação e comparações com os três baselines do README.

Produção usa antifraude@champion, Pipeline completo, threshold e motivo na versão, descrição, assinatura e exemplo. Código próprio deve acompanhar o modelo. A referência das semanas 11–12 deve ficar em referencia/ na run campeã.

Monitoramento: KS (D e p-valor) para contínuas e score; proporções ou qui-quadrado para categóricas, booleanas e hora; taxa e valor bloqueados; performance e custo global e por segmento após os rótulos. Relatório zero compara semanas 11 e 12. Limites de alerta devem ser justificados.

Entrega inclui notebook respondido e salvo, features.py, monitoramento.py, CHANGELOG v1.0.0, modelo e evidências exportadas.

## Fatos verificados por leitura

O pacote oferece aplicação FastAPI, contrato YAML, SQL, notebook e CSVs. features.py e monitoramento.py são esqueletos. Ainda não auditamos os CSVs nem executamos a aplicação.

## Questões abertas

Qual algoritmo e corte minimizam custo? O histórico respeita as regras semânticas? Quais alertas são estáveis? Existe infraestrutura local compatível sem interferir no turnover? Nenhuma dessas respostas está presumida.
