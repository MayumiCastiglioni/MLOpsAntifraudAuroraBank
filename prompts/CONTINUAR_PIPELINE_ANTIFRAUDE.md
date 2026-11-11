# Prompt padrão — avançar a pipeline antifraude com segurança

Trabalhe no repositório `C:\Users\mayumishimizu-ieg\OneDrive - Instituto Germinare\Área de Trabalho\3º ANO\Ciência de Dados II\Turnover novo\MLOpsAntifraudAuroraBank`, na branch `codex/experimentos-e-auditoria`. Leia `AGENTS.md`, `docs/status-etapas.md` e a documentação da próxima etapa antes de agir.

A usuária pediu avanço sequencial, status da demanda e que ações que precisem de aprovação sejam puladas e anotadas para discussão. Em cada execução, confira o estado atual e avance uma única próxima ação técnica segura, sem repetir trabalho concluído nem retreinar modelos já avaliados. Se uma etapa exigir uma decisão humana, registre opções, evidências e consequências em `docs/status-etapas.md` e `docs/decisoes/`, pule essa decisão e siga para a próxima etapa que possa avançar com segurança. Não repita uma pendência já registrada. O cron é para avançar a pipeline e reportar status, não para refazer os modelos a cada intervalo.

Pode executar análise, código local e verificações reproduzíveis sem aprovação adicional. Preserve os dados, banco do projeto Turnover e servidor MLflow existente. Nunca apague arquivos ou bases existentes. Não publique dados brutos, credenciais ou modelos no Git.

Se uma etapa exigir escolha de negócio, confirmação humana, mudança de política, promover ou mover o alias `champion`, ou outra aprovação, não faça essa ação. Faça as partes seguras da etapa, documente a decisão pendente, as opções, evidências e consequências em `docs/status-etapas.md` e `docs/decisoes/`, e reporte que aguarda discussão. Continue tarefas técnicas seguras que não dependam da decisão.

Ao finalizar uma etapa, atualize status e evidências, rode apenas verificações pertinentes, revise `git diff`, faça commit e push na branch de trabalho. Reporte em português: etapa concluída, evidências, etapa pendente, bloqueios que exigem decisão humana e links dos arquivos. Não alegue produção ou entrega concluída sem executar e verificar esses passos.
