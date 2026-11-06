# Notebook executado e pacote local de análise

## Escopo

`notebooks/01_analise_e_escolha.ipynb` é o notebook completo da análise e seleção: lê CSVs originais, audita contrato e junção, divide semanas, mostra funções reutilizáveis, declara cinco hipóteses, retreina os modelos, testa 99 cortes, compara baselines e semanas, recarrega o modelo e gera a justificativa final.

Não depende dos resultados JSON anteriores para escolher o candidato. Quando as evidências originais estão disponíveis, compara custos e cortes para conferir reprodução. Tempos variam por máquina. A execução integral foi planejada para o kernel Aurora MLOps (Python 3.11), com versões em requirements.reproducao.txt.

`parte1.ipynb` mantém o roteiro amplo da atividade em andamento; monitoramento baseline, promoção e paridade com API ainda não foram concluídos. O notebook de análise não declara essas etapas prontas.

## Reprodução no repositório

1. Instale requirements.reproducao.txt em ambiente virtual de caminho curto.
2. Registre o kernel com `python -m ipykernel install --user --name aurora-mlops --display-name "Aurora MLOps (Python 3.11)"` usando o Python desse ambiente.
3. Disponibilize os dois CSVs originais em dados/.
4. Abra notebooks/01_analise_e_escolha.ipynb, reinicie o kernel e execute todas as células.

Para montar uma cópia local independente e executá-la automaticamente: `python scripts/executar_notebook_analise.py`. O script não apaga entregas: cria uma nova pasta com data UTC dentro de entrega/. Essa cópia contém os dados locais do professor, sem credenciais e sem publicar CSVs no Git.

O MLflow usa por padrão diretório temporário local, sem Postgres ou servidor. A variável opcional AURORA_TRACKING_URI permite informar servidor; não há promoção automática. Cada execução tem experimento separado e arquivos em resultados_reproducao/<execucao>/.

## Conteúdo da pasta de entrega

- 01_analise_e_escolha.ipynb: código e saídas executadas, com justificativa na última célula.
- 01_analise_e_escolha.html: prévia para leitura sem Jupyter, quando nbconvert está disponível.
- RESUMO_ESCOLHA.md: justificativa final gerada a partir das métricas efetivas.
- LEIA_PRIMEIRO.md: instruções e limites da entrega.
- features.py, monitoramento.py, contrato/ e requirements.reproducao.txt: código e ambiente necessários.
- dados/: os CSVs originais, apenas na cópia local ignorada pelo Git.
- evidencias/ e documentacao/: rodada anterior, falha técnica e decisões.
- resultados_reproducao/: manifesto com hashes e versões, métricas, curvas e run_ids desta nova execução.
- VERIFICACAO_EXECUCAO.json: quantidade de células executadas e ausência de outputs de erro.

Não executar a célula original de exportação do professor sobre uma pasta entrega/ com arquivos manuais sem revisão: ela recria essa pasta. O gerador de snapshot desta análise não remove pastas existentes.
