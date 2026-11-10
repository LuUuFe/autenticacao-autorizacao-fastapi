import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import Token

CHAVE_JWT = os.getenv("JWT_SECRET", "")
if len(CHAVE_JWT.encode()) < 32:
    raise RuntimeError("Defina JWT_SECRET com uma chave de pelo menos 32 bytes.")

ALGORITMO = "HS256"
HASH_FALSO = pbkdf2_sha256.using(rounds=600_000).hash("senha-de-exemplo")

router = APIRouter(tags=["Autenticação"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


def credenciais_invalidas():
    return HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )


def buscar_usuario(db: Session, email: str):
    return db.scalar(select(Usuario).where(Usuario.email == email))


@router.post("/login", response_model=Token)
def login(
    formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    resposta: Response,
):
    if len(formulario.password) > 1024:
        raise credenciais_invalidas()

    usuario = buscar_usuario(db, formulario.username.strip().lower())
    senha_hash = usuario.senha_hash if usuario else HASH_FALSO
    if not pbkdf2_sha256.verify(formulario.password, senha_hash) or usuario is None:
        raise credenciais_invalidas()

    expira_em = datetime.now(timezone.utc) + timedelta(minutes=30)
    token = jwt.encode(
        {"sub": usuario.email, "exp": expira_em}, CHAVE_JWT, algorithm=ALGORITMO
    )
    resposta.headers["Cache-Control"] = "no-store"
    resposta.headers["Pragma"] = "no-cache"
    return {"access_token": token, "token_type": "bearer"}


def usuario_autenticado(
    token: Annotated[str, Depends(oauth2)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        dados = jwt.decode(
            token, CHAVE_JWT, algorithms=[ALGORITMO], options={"require": ["sub", "exp"]}
        )
    except jwt.InvalidTokenError:
        raise credenciais_invalidas() from None

    usuario = buscar_usuario(db, dados["sub"])
    if usuario is None:
        raise credenciais_invalidas()
    return usuario
