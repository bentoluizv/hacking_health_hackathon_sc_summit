from datetime import date
from http import HTTPStatus

from hackathon.schemas import PacienteModel


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
