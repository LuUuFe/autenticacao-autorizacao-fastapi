# API de Tarefas

**Integrante:** Luis Felipe Andrade Dias

CRUD de tarefas com FastAPI, SQLAlchemy, SQLite e migrações Alembic.

## Como executar

Requer Python 3.12+. Após clonar o repositório, entre na pasta e execute no Bash (Git Bash no Windows):

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

No Linux/macOS, crie o ambiente com `python3 -m venv .venv` e ative com
`source .venv/bin/activate`. Depois, execute os mesmos comandos de instalação,
migração e inicialização acima.

Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para testar as rotas.

## Uso

As rotas `/tarefas` e `/tarefas/{id}` permitem criar, listar, consultar,
atualizar (PUT) e excluir tarefas. Exemplo de corpo para criação ou atualização:

```json
{"titulo": "Estudar migrações", "descricao": "Revisar Alembic", "concluida": false}
```

O Alembic cria o banco `tarefas.db`, ignorado pelo Git. Os dados permanecem
após reiniciar a API. As migrações estão em `alembic/versions/`.
