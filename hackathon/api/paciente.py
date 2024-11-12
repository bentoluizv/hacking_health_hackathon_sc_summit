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
from hackathon.utils.to_tb import paciente_model_to_orm

router = APIRouter(
    prefix='/api/v1/pacientes',
    tags=['Paciente'],
    dependencies=[],
)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PacienteModel)
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

        paciente_orm = paciente_model_to_orm(paciente_model)

        session.add(paciente_orm)

        session.commit()

        return paciente_orm

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


@router.get(
    '/{documento}',
    status_code=HTTPStatus.OK,
    response_model=PacienteModel,
)
def buscar_paciente_por_documento(
    documento: str, session: Annotated[Session, Depends(get_session)]
):
    try:
        paciente_orm = session.scalar(
            select(PacienteOrm).where(PacienteOrm.documento == documento)
        )

        if not paciente_orm:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Paciente não encontrado',
            )

        paciente_model = PacienteModel(
            id=paciente_orm.id,
            documento=paciente_orm.documento,
            nome=paciente_orm.nome,
            data_nascimento=paciente_orm.data_nascimento,
        )

        return paciente_model

    except SQLAlchemyError:
        raise HTTPException(status_code=BAD_REQUEST)
