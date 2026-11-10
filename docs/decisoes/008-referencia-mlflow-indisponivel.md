# 008 — Referência E03 preparada localmente

Data: 10/11/2026. Estado: concluída em 10/11/2026; run original recuperada e artefatos anexados.

## Decisão e evidência

O usuário pediu prosseguir com a referência do modelo. Reutilizamos o artefato persistido da run E03 e reprocessamos as semanas 11–12 sem retreino. O CSV local contém ID da transação, semana, 13 features, score, decisão no threshold 0,10 e rótulo. São 39.497 linhas; custos recalculados: semana 11 R$ 11.019,25 e semana 12 R$ 7.966,36. Hashes e métricas estão em `docs/evidencias/referencia-e03-preparada.json`; o gerador é `scripts/preparar_referencia_e03.py`.

## Verificação

Após o usuário iniciar o container `pg`, reiniciamos o MLflow 2.19.0 no endpoint local já configurado. Anexamos o CSV e manifesto à mesma run E03, sob `referencia/`, confirmamos os dois caminhos via MlflowClient e baixamos o CSV novamente. O SHA-256 baixado coincide com o manifesto local. Sem retreino e sem mudança de alias.

## Próximo passo

Registrar candidato/política e discutir promoção de `champion` separadamente; a troca de produção aguarda validação humana.
