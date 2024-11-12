from datetime import date, datetime
from http import HTTPStatus

from hackathon.models import PacienteOrm
from hackathon.schemas import AtendimentoModel, PacienteModel


def test_deve_criar_um_paciente(client):
    paciente_model = PacienteModel(
        documento='5622440', nome='Bento', data_nascimento=date(1989, 4, 4)
    )

    res = client.post(
        '/api/v1/pacientes', data=paciente_model.model_dump_json()
    )

    paciente = res.json()

    assert res.status_code == HTTPStatus.CREATED
    assert paciente['id']
