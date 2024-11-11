from datetime import date, datetime
from http import HTTPStatus

from hackathon.models import PacienteOrm
from hackathon.schemas import AtendimentoModel, PacienteModel


def test_deve_criar_um_paciente(client):
    paciente_model = PacienteModel(
        documento='5622440', nome='Bento', data_nascimento=date(1989, 4, 4)
    )

    res = client.post('/paciente', data=paciente_model.model_dump_json())

    assert res.status_code == HTTPStatus.CREATED


def test_deve_criar_um_atendimento(client, session):
    paciente_model = PacienteModel(
        documento='5622440', nome='Bento', data_nascimento=date(1989, 4, 4)
    )

    paciente_orm = PacienteOrm(
        documento=paciente_model.documento,
        nome=paciente_model.nome,
        data_nascimento=paciente_model.data_nascimento,
    )

    session.add(paciente_orm)
    session.commit()

    atendimento_model = AtendimentoModel(
        paciente=paciente_model,
        data=datetime.now(),
        consultas=None,
        evolucoes=None,
        triagem=None,
    )

    res = client.post('/atendimento', data=atendimento_model.model_dump_json())

    assert res.status_code == HTTPStatus.CREATED
