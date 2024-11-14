from http import HTTPStatus

from hackathon.api.triagem import Input
from hackathon.schemas import TriagemModel


def test_triagem_api(client):
    triagem_text = """Durante a triagem, o paciente apresentou-se com queixa de
                    dor no peito, relatando início dos sintomas em 08/11/2024.
                    Ele descreve a dor como contínua e localizada no centro do
                    peito, acompanhada de sensação de falta de ar. Ao ser
                    questionado sobre a intensidade da dor, classificou-a como
                    8 em uma escala de 0 a 10, indicando dor intensa. O
                    paciente possui histórico de diabetes tipo 2, hipertensão
                    arterial e asma. Em relação ao histórico familiar, relatou
                    que sua mãe apresenta problemas cardíacos e sua avó materna
                    teve câncer de mama. Foram realizadas as seguintes
                    aferições de sinais vitais: pressão arterial de 120/80
                    mmHg, frequência cardíaca de 85 bpm, saturação de oxigênio
                    de 97%, temperatura corporal de 36,7°C e frequência
                    respiratória de 18 respirações por minuto. Devido à queixa
                    de dor no peito intensa e a presença de falta de ar, foi
                    atribuída ao paciente uma classificação de urgência alta,
                    justificando prioridade de atendimento imediato para
                    investigar possíveis condições graves."""

    input = Input(triagem_text=triagem_text)

    response = client.post('/api/v1/triagem', data=input.model_dump_json())

    data = response.json()

    triagem = TriagemModel(**data)

    assert response.status_code == HTTPStatus.OK

    assert triagem.inicio_sintoma == '08/11/2024'  # type: ignore

    assert (
        triagem.historico_individual
        == 'diabetes tipo 2, hipertensão arterial e asma'
    )

    assert (
        triagem.historico_familiar
        == 'mãe: problemas cardíacos; avó materna: câncer de mama'
    )
    assert triagem.sinais_vitais.temperatura == '36,7°C'  # type: ignore
