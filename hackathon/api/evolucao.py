from http import HTTPStatus
from typing import Annotated

from click import echo
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hackathon.db import get_session

router = APIRouter(
    prefix='/evolucao',
    tags=['Evolução Enfermagem'],
    dependencies=[],
)


class Input(BaseModel):
    atendimento_id: int
    data: str


@router.post('/', status_code=HTTPStatus.CREATED, response_model=None)
def criar_nova_evolucao(
    data: Input,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        echo(data)

    except SQLAlchemyError:
        session.rollback()
