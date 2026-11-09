from fastapi import FastAPI

from app.routes import router
from app.seguranca import router as router_login

app = FastAPI(
    title="API de Tarefas",
    description="Cadastro de tarefas com SQLite e autenticação por JWT.",
    version="1.0.0",
)
app.include_router(router_login)
app.include_router(router)
