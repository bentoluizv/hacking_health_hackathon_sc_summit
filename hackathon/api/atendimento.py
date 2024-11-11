from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hackathon.db import get_session
from hackathon.models import AtendimentoOrm, PacienteOrm
from hackathon.schemas import (
    AtendimentoModel,
    ConsultaModel,
    DiagnosticoModel,
    EvolucaoEnfermagemModel,
    ExameModel,
    MedicamentoModel,
    MotivoModel,
    PacienteModel,
    ProcedimentoModel,
    SinaisVitaisModel,
    TriagemModel,
)

router = APIRouter(
    prefix='/atendimento',
    tags=['Atendimento'],
    dependencies=[],
)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=None)
def criar_novo_atendimento(
    atendimento: AtendimentoModel,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        paciente_orm = session.scalar(
            select(PacienteOrm).where(
                PacienteOrm.documento == atendimento.paciente.documento
            )
        )

        if not paciente_orm:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        atendimento_orm = AtendimentoOrm(
            paciente_id=paciente_orm.id, paciente=paciente_orm
        )

        session.add(atendimento_orm)

        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f'Error: {str(e)}')
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Erro ao criar o atendimento.',
        )


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=List[AtendimentoModel]
)
def listar_atendimentos(session: Annotated[Session, Depends(get_session)]):
    try:
        atendimentos_orm = session.scalars(select(AtendimentoOrm)).all()

        for atendimento_orm in atendimentos_orm:
            paciente_model = PacienteModel(
                id=atendimento_orm.paciente.id,
                documento=atendimento_orm.paciente.documento,
                nome=atendimento_orm.paciente.nome,
                data_nascimento=atendimento_orm.paciente.data_nascimento,
            )

            triagem_model = TriagemModel(
                id=atendimento_orm.triagem.id,
                historico_individual=atendimento_orm.triagem.historico_individual,
                historico_familiar=atendimento_orm.triagem.historico_familiar,
                motivo=MotivoModel(
                    id=atendimento_orm.triagem.motivo.id,
                    inicio=atendimento_orm.triagem.motivo.inicio,
                    sintoma=atendimento_orm.triagem.motivo.sintoma,
                    localizacao=atendimento_orm.triagem.motivo.localizacao,
                    sintomas_associados=atendimento_orm.triagem.motivo.sintomas_associados,
                ),
                escala_dor=atendimento_orm.triagem.escala_dor,
                urgencia=atendimento_orm.triagem.urgencia,
                sinais_vitais=[
                    SinaisVitaisModel(
                        id=sinais_vitais_orm.id,
                        pressao_arterial=sinais_vitais_orm.pressao_arterial,
                        temperatura=sinais_vitais_orm.temperatura,
                        frequencia_cardiaca=sinais_vitais_orm.frequencia_cardiaca,
                        frequencia_respiratoria=sinais_vitais_orm.frequencia_respiratoria,
                    )
                    for sinais_vitais_orm in atendimento_orm.triagem.sinais_vitais  # noqa: E501
                ],
            )

            consultas_model = [
                ConsultaModel(
                    id=consulta_orm.id,
                    data_hora=consulta_orm.data_hora,
                    diagnostico_inicial=DiagnosticoModel(
                        id=consulta_orm.diagnostico.id,
                        condicao_principal=consulta_orm.diagnostico.condicao_principal,
                        diagnostico_diferencial=consulta_orm.diagnostico.diagnostico_diferencial.split(
                            ','  # TODO: refatorar essa porcaria
                        ),
                    ),
                    orientacoes=consulta_orm.orientacoes,
                    urgencia=consulta_orm.urgencia,
                    procedimentos_realizados=[
                        ProcedimentoModel(
                            id=procedimento_orm.id,
                            nome=procedimento_orm.nome,
                            data_solicitacao=procedimento_orm.data_solicitacao,
                            tipo=procedimento_orm.tipo,
                        )
                        for procedimento_orm in consulta_orm.procedimentos_realizados  # noqa: E501
                    ],
                    exames_solicitados=[
                        ExameModel(
                            id=exame_orm.id,
                            nome_exame=exame_orm.nome,
                            data_solicitacao=exame_orm.data_solicitacao,
                            resultado=exame_orm.resultado,
                            status=exame_orm.status.value,
                            tipo=exame_orm.tipo,
                        )
                        for exame_orm in consulta_orm.exames_solicitados
                    ],
                    medicamentos_prescritos=[
                        MedicamentoModel(
                            id=medicamento_orm.id,
                            nome=medicamento_orm.nome,
                            dose=medicamento_orm.dose,
                            via_administracao=medicamento_orm.via_administracao,
                            frequencia=medicamento_orm.frequencia,
                            duracao=medicamento_orm.duracao,
                        )
                        for medicamento_orm in consulta_orm.medicamentos_prescritos  # noqa: E501
                    ],
                )
                for consulta_orm in atendimento_orm.consultas
            ]

            evolucoes_model = [
                EvolucaoEnfermagemModel(
                    id=evolucao_enfermagem_orm.id,
                    data_hora=evolucao_enfermagem_orm.data_hora,
                    observacoes=evolucao_enfermagem_orm.observacoes,
                    procedimentos_realizados=[
                        ProcedimentoModel(
                            id=procedimento_orm.id,
                            nome=procedimento_orm.nome,
                            data_solicitacao=procedimento_orm.data_solicitacao,
                            tipo=procedimento_orm.tipo,
                        )
                        for procedimento_orm in evolucao_enfermagem_orm.procedimentos_realizados  # noqa: E501
                    ],
                    resposta_ao_tratamento=evolucao_enfermagem_orm.resposta_ao_tratamento,
                    sinais_vitais=[
                        SinaisVitaisModel(
                            id=evolucao_orm.id,
                            pressao_arterial=evolucao_orm.pressao_arterial,
                            frequencia_cardiaca=evolucao_orm.frequencia_cardiaca,
                            frequencia_respiratoria=evolucao_orm.frequencia_respiratoria,
                            temperatura=evolucao_orm.temperatura,
                        )
                        for evolucao_orm in evolucao_enfermagem_orm.sinais_vitais  # noqa: E501
                    ],
                )
                for evolucao_enfermagem_orm in atendimento_orm.evolucoes
            ]

            atendimento_model = AtendimentoModel(
                id=atendimento_orm.id,
                data=atendimento_orm.data,
                paciente=paciente_model,
                triagem=triagem_model,
                consultas=consultas_model,
                evolucoes=evolucoes_model,
            )

        return atendimento_model

    except SQLAlchemyError:
        session.rollback()
