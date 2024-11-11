from http import HTTPStatus
from http.client import BAD_REQUEST
from typing import Annotated, List

from click import echo
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hackathon.db import get_session
from hackathon.models import PacienteOrm
from hackathon.schemas import PacienteModel

router = APIRouter(
    prefix='/paciente',
    tags=['Paciente'],
    dependencies=[],
)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=None)
def criar_novo_paciente(
    paciente_model: PacienteModel,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        exists = session.scalar(
            select(PacienteOrm).where(
                PacienteOrm.documento == paciente_model.documento
            )
        )

        if exists:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        paciente_orm = PacienteOrm(
            data_nascimento=paciente_model.data_nascimento,
            documento=paciente_model.documento,
            nome=paciente_model.nome,
        )

        session.add(paciente_orm)

        session.commit()

    except SQLAlchemyError as Error:
        echo(Error)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@router.get('/', status_code=HTTPStatus.OK, response_model=List[PacienteModel])
def listar_pacientes(session: Annotated[Session, Depends(get_session)]):
    try:
        pacientes_orm = session.scalars(select(PacienteOrm)).all()

        pacientes_model = [
            PacienteModel(
                id=paciente_orm.id,
                documento=paciente_orm.documento,
                nome=paciente_orm.nome,
                data_nascimento=paciente_orm.data_nascimento,
            )
            for paciente_orm in pacientes_orm
        ]

        return pacientes_model

    except SQLAlchemyError:
        raise HTTPException(status_code=BAD_REQUEST)
