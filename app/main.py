from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="API de Tarefas",
    description="Cadastro de tarefas com persistência em SQLite e migrações Alembic.",
    version="1.0.0",
)
app.include_router(router)
