# fin-data-platform

Protótipo de plataforma de dados financeiros. O projeto simula a ingestão de lançamentos de um ERP, guarda os dados em um banco PostgreSQL, expõe uma API REST e mostra tudo em um dashboard web.

## O que o projeto faz

1. **Extrai** lançamentos financeiros de uma fonte (hoje, um ERP simulado com 3 registros fixos: duas vendas e uma despesa).
2. **Carrega** os dados na tabela `raw_financial` do PostgreSQL. A carga é idempotente: cada lançamento tem um `external_id` único, então rodar o pipeline várias vezes não duplica registros.
3. **Expõe** os dados por uma API FastAPI (lista paginada e resumo de receitas, despesas e saldo).
4. **Exibe** um dashboard React com cards de totais, gráfico de barras por lançamento e tabela paginada.

```
ERP simulado -> pipeline (extract + load) -> PostgreSQL -> API FastAPI -> Dashboard React
```

## Estrutura

```
backend/
  app/main.py            API FastAPI (endpoints e CORS)
  db/connection.py       engine, sessão e get_db (lê DATABASE_URL)
  db/models.py           modelo RawFinancial
  db/create_tables.py    init_db(): cria as tabelas
pipeline/
  extract/extract_erp.py extração (ERP simulado)
  load/load_raw.py       carga idempotente no banco
  jobs/run_pipeline.py   executa extração + carga
frontend/                Dashboard (Vite + React + TypeScript)
tests/                   Testes (pytest)
docker-compose.yml       Postgres, API, front e job do pipeline
```

## Pré-requisitos

- **Para rodar com Docker (recomendado):** Docker Desktop.
- **Para desenvolvimento local:** Docker (para o banco), Python 3.12+ e Node 20+.

## Como rodar (tudo em Docker)

Na raiz do projeto:

```
copy .env.example .env
```

Abra o `.env` e defina a senha do banco. `POSTGRES_PASSWORD` e a senha dentro de `DATABASE_URL` devem ser iguais.

Depois:

```
docker compose up -d --build
docker compose run --rm pipeline
```

O primeiro comando sobe o banco, a API e o front. O segundo carrega os dados no banco; pode ser repetido sem duplicar nada.

Acesse:

| Serviço   | Container    | URL                            |
|-----------|--------------|--------------------------------|
| Dashboard | fin-data-web | http://localhost:5173          |
| API (docs)| fin-data-api | http://localhost:8000/docs     |
| Postgres  | fin-data     | localhost:5432, banco `findata`|

Comandos úteis:

| Ação                               | Comando                                                |
|------------------------------------|--------------------------------------------------------|
| Ver logs                           | `docker compose logs -f api`                           |
| Parar                              | `docker compose stop`                                  |
| Subir de novo                      | `docker compose up -d`                                 |
| Rebuild após mudar código          | `docker compose up -d --build`                         |
| Apagar tudo, inclusive os dados    | `docker compose down -v`                               |
| Abrir o psql                       | `docker exec -it fin-data psql -U postgres -d findata` |

## Como rodar em desenvolvimento local

Útil para editar código com recarga automática. O banco continua no Docker.

```
docker compose up -d db
```

**Backend** (em um terminal, na raiz):

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pipeline.jobs.run_pipeline
uvicorn backend.app.main:app --reload
```

**Frontend** (em outro terminal):

```
cd frontend
copy .env.example .env
npm install
npm run dev
```

Se o front rodar em outra porta que não a 5173, ajuste `allow_origins` em `backend/app/main.py`.

## Configuração

| Variável            | Onde           | Descrição                                         |
|---------------------|----------------|---------------------------------------------------|
| `POSTGRES_PASSWORD` | `.env` (raiz)  | Senha do Postgres (usada pelo docker-compose)     |
| `DATABASE_URL`      | `.env` (raiz)  | URL de conexão, ex.: `postgresql+psycopg2://postgres:SENHA@localhost:5432/findata` |
| `VITE_API_URL`      | `frontend/.env`| Endereço da API usado pelo front                  |

O `.env` não vai para o git. Use o `.env.example` como modelo. A URL usa o driver `postgresql+psycopg2` de propósito: sem o sufixo, o SQLAlchemy 2.1 tenta usar o `psycopg` (v3), que não está instalado.

No Docker, a API e o pipeline recebem a `DATABASE_URL` apontando para o host `db`, definida no `docker-compose.yml`. O `VITE_API_URL` é embutido no build do front; ao mudá-lo, rebuilde com `docker compose up -d --build web`.

## API

| Método e rota                            | Descrição                                           |
|------------------------------------------|-----------------------------------------------------|
| `GET /health`                            | Verifica se a API está no ar                        |
| `GET /financial?limit=100&offset=0`      | Lista lançamentos (limit de 1 a 1000)               |
| `GET /financial/summary`                 | Receitas, despesas, saldo e quantidade de lançamentos |

Exemplo de resposta de `/financial/summary`:

```
{"income": 1500.0, "expenses": -300.0, "balance": 1200.0, "count": 3}
```

## Testes

```
venv\Scripts\activate
pytest
```

Os testes usam SQLite temporário, então não precisam do Postgres. Cobrem a extração, a carga (incluindo idempotência) e os endpoints da API.

## Problemas comuns

- **"DATABASE_URL não definida":** o `.env` não existe na raiz. Copie o `.env.example`.
- **"Can't load plugin / No module named psycopg":** a `DATABASE_URL` está sem o `+psycopg2` depois de `postgresql`.
- **Dashboard mostra erro de carregamento:** a API não está no ar ou o CORS não libera a origem do front. Confira `http://localhost:8000/health`.
- **Porta 5432, 8000 ou 5173 em uso:** pare o processo que a ocupa ou mude o mapeamento de portas no `docker-compose.yml`.
- **Mudei o modelo e a tabela não atualizou:** `create_all` não altera tabelas existentes. Em desenvolvimento, use `docker compose down -v` para recriar o banco.
# fin-data-platform
