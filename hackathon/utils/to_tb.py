from hackathon.models import PacienteOrm
from hackathon.schemas import PacienteModel


def paciente_model_to_orm(paciente: PacienteModel) -> PacienteOrm:
    paciente_orm = PacienteOrm(
        documento=paciente.documento,
        nome=paciente.nome,
        data_nascimento=paciente.data_nascimento,
    )
    return paciente_orm


def paciente_orm_to_model(paciente: PacienteOrm) -> PacienteModel:
    paciente_model = PacienteModel(
        id=paciente.id,
        documento=paciente.documento,
        nome=paciente.nome,
        data_nascimento=paciente.data_nascimento,
    )
    return paciente_model
