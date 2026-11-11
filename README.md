# API de Tarefas

**Integrante:** Luis Felipe Andrade Dias

API de tarefas com FastAPI, SQLite, migrações Alembic e autenticação OAuth2 com JWT.

## Como executar

Requer Python 3.12 ou superior. Depois de clonar o repositório, entre na pasta do projeto.

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m app.criar_usuario
$env:JWT_SECRET = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
alembic upgrade head
python -m app.criar_usuario
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
uvicorn app.main:app --reload
```

O comando `criar_usuario` pede um e-mail e uma senha de pelo menos 8 caracteres.
O banco `tarefas.db` é criado pelo Alembic e fica fora do Git. Somente o hash da senha é salvo.

## Como testar no Swagger

1. Abra [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Execute `GET /tarefas` sem login.
2. Tente executar `POST /tarefas` sem se autenticar. A API deve retornar `401`.
3. Clique em **Authorize**. Em `username`, informe o e-mail cadastrado; em `password`, informe a senha. Deixe `client_id` e `client_secret` vazios e confirme em **Authorize**.
4. Execute `POST /tarefas` novamente. Use o ID retornado para testar `PUT /tarefas/{tarefa_id}` e `DELETE /tarefas/{tarefa_id}`.

Exemplo de corpo para criar ou atualizar uma tarefa:

```json
{"titulo": "Estudar FastAPI", "descricao": "Revisar autenticação", "concluida": false}
```

O Swagger chama `POST /login` e envia `Authorization: Bearer <token>` nas rotas protegidas. Para ver o JWT, execute `POST /login` diretamente no Swagger e confira o campo `access_token` na resposta. O token expira em 30 minutos.
