# Reprodução dos notebooks e dos serviços

Este roteiro distingue a reprodução da análise offline da inicialização da aplicação com Postgres, MLflow e API. Os exemplos são para PowerShell no Windows e Python 3.11.

## 1. Dependências e configuração

Na raiz do projeto, crie um ambiente Python fora da pasta sincronizada se o caminho do projeto for longo:

```powershell
$venv = "$env:USERPROFILE\.venvs\aurora-mlops"
py -3.11 -m venv $venv
$python = "$venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
Copy-Item .env.exemplo .env
```

Edite `.env` para corresponder ao Postgres local. Para os serviços deste projeto, use `MLFLOW_TRACKING_URI=http://127.0.0.1:5001` e `SISTEMA_URL=http://127.0.0.1:8001`. Não versionar `.env`.

## 2. Iniciar Postgres sem interferir em outros projetos

### Reaproveitar o container local já configurado

Se o container `pg` já existe e contém os bancos deste projeto, inicie-o e confira a prontidão:

```powershell
docker start pg
docker exec pg pg_isready -U postgres
```

Não remova o container ou volume. Se estiver ativo, `docker start pg` pode informar que já está iniciado; confirme com `docker ps`.

### Criar um ambiente Postgres isolado em uma máquina nova

Use esta opção somente para uma instância nova e isolada. Ela expõe o Postgres na porta 5433 para evitar conflito com o container `pg` existente:

```powershell
docker run --name aurora-pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5433:5432 -v aurora_pgdata:/var/lib/postgresql/data -d postgres:16
docker exec aurora-pg pg_isready -U postgres
docker cp sql/01_criar_bancos.sql aurora-pg:/tmp/01_criar_bancos.sql
docker exec aurora-pg psql -U postgres -f /tmp/01_criar_bancos.sql
docker cp sql/02_criar_tabelas.sql aurora-pg:/tmp/02_criar_tabelas.sql
docker exec aurora-pg psql -U postgres -d antifraude -f /tmp/02_criar_tabelas.sql
```

Neste caso, ajuste `.env` para `PG_PORT=5433`, `PG_USER=postgres`, `PG_SENHA=postgres`, `PG_DB_APP=antifraude` e `PG_DB_MLFLOW=mlflow`. `sql/01_criar_bancos.sql` cria os dois bancos uma vez; pule essa etapa se eles já existem. O MLflow cria as próprias tabelas no banco `mlflow` ao iniciar.

## 3. MLflow e API

Abra dois terminais na raiz do repositório e use o mesmo `$python` do ambiente virtual.

Terminal 1 — servidor de tracking e Model Registry:

```powershell
& $python scripts/servir_mlflow.py
```

Ele usa o banco `mlflow`, escuta em `127.0.0.1:5001` e grava artefatos em `mlruns/`.

Terminal 2 — API e interface web:

```powershell
& $python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Confirme os serviços em um terceiro terminal:

```powershell
Invoke-WebRequest http://127.0.0.1:5001/health
Invoke-RestMethod http://127.0.0.1:8001/saude
Invoke-RestMethod http://127.0.0.1:8001/api/modelo
```

Para o estado desta entrega, a saúde da API deve indicar modelo disponível, versão `1`, threshold `0.1` e run `ff48c43154624ec9a1e3d16688909ef3`. Também é possível rodar `& $python scripts/preparar_entrega_final.py --check-only` para checar alias, tags, referência, dados e API antes da exportação.

### Restaurar em uma instalação realmente vazia

O ZIP contém o pipeline exportado, a referência e evidências, mas não inclui dump do banco Postgres/MLflow nem credenciais. Por isso, iniciar MLflow sobre um banco vazio não recria o histórico, run ID, versão ou alias `champion`; a API informará que não há modelo até que um modelo seja registrado e promovido. Para restaurar exatamente o estado registrado, é necessário um backup compatível dos bancos `mlflow` e `antifraude` e dos artefatos correspondentes. Uma nova instalação a partir apenas do modelo exportado pode ser funcional, mas cria nova linhagem e exige registro/promoção explícitos; não deve ser apresentada como a run histórica original. Nenhum script desta entrega move o alias automaticamente ao iniciar.

## 4. Notebook de análise reproduzível

O notebook `notebooks/01_analise_e_escolha.ipynb` não precisa dos serviços de produção. Com os CSVs disponíveis em `dados/`, selecione o kernel Python 3.11 com `requirements.txt` e execute Run All. Para criar um snapshot executado com métricas, curvas e manifesto, rode:

```powershell
& $python scripts/executar_notebook_analise.py
```

Isso retreina as cinco famílias e cria novas runs; não promove modelo. Cada execução salva seus resultados sem apagar as anteriores. Execute a partir de um ZIP extraído se quiser comprovar a ausência de dependência de `.git`.

## 5. Notebook da atividade e pacote

`parte1.ipynb` consulta serviços de produção, por isso depende das etapas 1–3. Depois de executar todas as células, salve o notebook e gere um novo snapshot:

```powershell
& $python scripts/preparar_entrega_final.py
```

O gerador cria uma nova pasta e um ZIP com timestamp em `entrega/` e na raiz do projeto, preserva snapshots existentes e registra avisos no `VERIFICACAO_ENTREGA.json`. Ele não apaga bancos, não promove modelos e não inclui `.env`, credenciais ou logs.

As semanas 11–12 foram usadas na escolha do modelo e do corte; seus resultados são validação de seleção, não teste independente.
