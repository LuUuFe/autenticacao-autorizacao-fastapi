from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tarefa
from app.schemas import TarefaDados, TarefaResposta

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])
SessionDep = Annotated[Session, Depends(get_db)]


def buscar_tarefa(tarefa_id: int, db: Session) -> Tarefa:
    tarefa = db.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.post("", response_model=TarefaResposta, status_code=status.HTTP_201_CREATED)
def criar_tarefa(dados: TarefaDados, db: SessionDep):
    tarefa = Tarefa(**dados.model_dump())
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.get("", response_model=list[TarefaResposta])
def listar_tarefas(
    db: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    concluida: bool | None = None,
):
    consulta = select(Tarefa).order_by(Tarefa.id)
    if concluida is not None:
        consulta = consulta.where(Tarefa.concluida == concluida)
    return db.scalars(consulta.offset(offset).limit(limit)).all()


@router.get("/{tarefa_id}", response_model=TarefaResposta)
def obter_tarefa(tarefa_id: int, db: SessionDep):
    return buscar_tarefa(tarefa_id, db)


@router.put("/{tarefa_id}", response_model=TarefaResposta)
def atualizar_tarefa(tarefa_id: int, dados: TarefaDados, db: SessionDep):
    tarefa = buscar_tarefa(tarefa_id, db)
    for campo, valor in dados.model_dump().items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tarefa(tarefa_id: int, db: SessionDep):
    tarefa = buscar_tarefa(tarefa_id, db)
    db.delete(tarefa)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
