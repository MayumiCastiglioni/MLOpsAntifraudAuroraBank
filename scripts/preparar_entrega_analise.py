"""Monta snapshot local de análise, sem apagar entregas ou expor credenciais."""
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]


def preparar():
    destino=ROOT/"entrega"/("analise_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    destino.mkdir(parents=True,exist_ok=False)
    arquivos={"notebooks/01_analise_e_escolha.ipynb":"01_analise_e_escolha.ipynb","features.py":"features.py","monitoramento.py":"monitoramento.py","requirements.reproducao.txt":"requirements.reproducao.txt","contrato/contrato_features.yaml":"contrato/contrato_features.yaml","dados/transacoes_semanas_01_12.csv":"dados/transacoes_semanas_01_12.csv","dados/rotulos_semanas_01_12.csv":"dados/rotulos_semanas_01_12.csv","docs/evidencias/experimentos-iniciais.json":"evidencias/experimentos-originais.json","docs/evidencias/tentativa-tecnica-inicial.json":"evidencias/tentativa-tecnica-inicial.json","docs/evidencias/auditoria-inicial.json":"evidencias/auditoria-inicial.json","docs/evidencias/auditoria-temporal.json":"evidencias/auditoria-temporal.json"}
    for origem,relativo in arquivos.items():
        target=destino/relativo;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/origem,target)
    shutil.copytree(ROOT/"docs",destino/"documentacao")
    (destino/"LEIA_PRIMEIRO.md").write_text("""# Entrega de análise — Banco Aurora

Esta pasta contém o notebook executado de auditoria, comparação e escolha do candidato. Não é a entrega integral da atividade: promoção, monitoramento e teste de API ainda estão pendentes.

## Leitura

1. Abra 01_analise_e_escolha.ipynb: todas as células devem ter contagem e saídas salvas. A última célula apresenta a justificativa final.
2. Leia RESUMO_ESCOLHA.md para a decisão em linguagem de negócio.
3. Consulte evidencias/, documentacao/ e resultados_reproducao/ para histórico e rastreabilidade. Os dados fornecidos pelo professor estão em dados/, localmente, sem publicação no Git.

## Reprodução

Use Python 3.11. Crie um ambiente virtual em um caminho curto, instale requirements.reproducao.txt e registre/selecione o kernel desse ambiente. Exemplos de comandos, executados na pasta desta entrega:

```text
python -m venv <caminho-curto-do-ambiente>
<python-do-ambiente> -m pip install -r requirements.reproducao.txt
<python-do-ambiente> -m ipykernel install --user --name aurora-mlops --display-name "Aurora MLOps (Python 3.11)"
<python-do-ambiente> -m notebook
```

Abra o notebook, reinicie o kernel Aurora MLOps e execute todas as células. Não precisa de Postgres, .env ou API. Por padrão, o MLflow é local em pasta temporária; cada execução mantém seus resultados em resultados_reproducao/<execucao> e cria novas runs. Não apaga bancos nem promove modelo. As dependências precisam ser instaladas antes da execução; tempos variam entre máquinas.

Os hashes dos dados são exibidos no notebook e gravados no manifesto. Cortes e custos são conferidos contra a rodada original; se alguma verificação falhar, investigue em vez de ignorar. A reprodução foi validada no ambiente registrado, sem alegar validação em todos os sistemas operacionais.

Os logs temporários locais do MLflow podem ser removidos pelo sistema operacional. Este pacote conserva resultados e manifesto; o notebook permite regenerar os treinos e as runs.
""",encoding="utf-8")
    return destino


if __name__=="__main__":print(preparar())
