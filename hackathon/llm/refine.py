import uuid
from typing import List, TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from pydantic import BaseModel

from hackathon.schemas import (
    SinaisVitaisModel,
    TriagemModel,
)

triagem_examples = [
    (
        """Durante a entrevista, o paciente se apresentou com dor no
           peito, referindo que a dor começou em 08/11/2024 e que é
           contínua, localizada no centro do peito, com sensação de falta
           de ar associada. Ele classificou a dor como intensa, marcando
           8 na escala de dor de 0 a 10. Relatou ter histórico de diabetes
           tipo 2, hipertensão arterial e asma. Em relação ao histórico
           familiar, informou que sua mãe tem problemas cardíacos e sua
           avó materna teve câncer de mama. A pressão arterial do paciente
           foi medida em 120/80 mmHg, com frequência cardíaca de 85 bpm,
           saturação de oxigênio em 97% e temperatura corporal em
           36,7°C. A frequência respiratória foi medida em 18
           respirações por minuto. O paciente foi classificado com
           urgência 9, dada a intensidade dos sintomas e a queixa de
           dor no peito com falta de ar, o que sugere uma possível
           condição grave.""",
        TriagemModel(
            id=None,
            sinais_vitais=SinaisVitaisModel(
                id=None,
                pressao_arterial='120/80 mmHg',
                frequencia_cardiaca='85 bpm',
                temperatura='36.7°C',
                saturacao_oxigenio='97%',
                frequencia_respiratoria='18 rpm',
            ),
            historico_individual='diabetes tipo 2, hipertensão arterial, asma',  # noqa: E501
            historico_familiar='doenças cardíacas (mãe), câncer de mama (avó materna)',  # noqa: E501
            inicio_sintoma='08/11/2024',
            sintoma_localizacao='centro do peito',
            sintoma='dor no peito',
            sintomas_associados='associada a falta de ar',
            escala_dor='8',
            urgencia='9',
        ),
    ),
    (
        """Durante a entrevista, o paciente se apresentou com dor
           abdominal intensa, que começou em 09/11/2024. A dor é
           localizada no quadrante inferior direito do abdômen, com
           náuseas associadas. Ele classificou a dor como 7 na escala de
           dor de 0 a 10. Relatou histórico de apendicite anterior, mas
           não apresenta outras condições de saúde. Em relação ao
           histórico familiar, informou que seu pai tem hipertensão e sua
           mãe tem diabetes. A pressão arterial foi medida em 130/85 mmHg,
           com frequência cardíaca de 90 bpm, saturação de oxigênio em
           98% e temperatura corporal em 37.2°C. A frequência respiratória
           foi medida em 20 respirações por minuto. A urgência foi
           classificada como 7, dado o quadro de dor intensa e náuseas.
                """,
        TriagemModel(
            id=None,
            sinais_vitais=SinaisVitaisModel(
                id=None,
                pressao_arterial='130/85 mmHg',
                frequencia_cardiaca='90 bpm',
                temperatura='37.2°C',
                saturacao_oxigenio='98%',
                frequencia_respiratoria='20 rpm',
            ),
            historico_individual='apendicite anterior',
            historico_familiar='hipertensão (pai), diabetes (mãe)',
            inicio_sintoma='09/11/2024',
            sintoma_localizacao='quadrante inferior direito do abdômen',
            sintoma='dor abdominal',
            sintomas_associados='náuseas',
            escala_dor='7',
            urgencia='7',
        ),
    ),
    (
        """Durante a entrevista, o paciente se apresentou com dor
           lombar aguda, referindo que a dor começou em 10/11/2024 e que é
           localizada na região inferior das costas, com irradiação para
           a perna direita. Ele classificou a dor como 6 na escala de
           dor de 0 a 10. Relatou histórico de hérnia de disco e
           fibromialgia. Não há histórico familiar relevante. A pressão
           arterial foi medida em 125/75 mmHg, com frequência cardíaca de
           80 bpm, saturação de oxigênio em 98% e temperatura corporal em
           36.5°C. A frequência respiratória foi medida em 16 respirações
           por minuto. A urgência foi classificada como 6, dada a dor
           moderada e o histórico de hérnia.""",
        TriagemModel(
            id=None,
            sinais_vitais=SinaisVitaisModel(
                id=None,
                pressao_arterial='125/75 mmHg',
                frequencia_cardiaca='80 bpm',
                temperatura='36.5°C',
                saturacao_oxigenio='98%',
                frequencia_respiratoria='16 rpm',
            ),
            historico_individual='hérnia de disco, fibromialgia',
            historico_familiar='nenhum relevante',
            inicio_sintoma='10/11/2024',
            sintoma_localizacao='região inferior das costas',
            sintoma='dor lombar',
            sintomas_associados='irradiação para a perna direita',
            escala_dor='6',
            urgencia='6',
        ),
    ),
    (
        """Durante a entrevista, o paciente se apresentou com dor de
           cabeça severa, iniciada em 11/11/2024, com sensação de pressão
           na região frontal. Ele relatou que a dor é contínua e se
           intensifica com movimentos rápidos da cabeça. Classificou a
           dor como 9 na escala de dor de 0 a 10. O paciente tem histórico
           de enxaqueca. Em relação ao histórico familiar, informou que
           sua mãe sofre de enxaqueca crônica. A pressão arterial foi
           medida em 115/75 mmHg, com frequência cardíaca de 70 bpm,
           saturação de oxigênio em 99% e temperatura corporal em 36.8°C.
           A frequência respiratória foi medida em 14 respirações por
           minuto. A urgência foi classificada como 6, considerando a dor
           intensa e o histórico de enxaqueca.""",
        TriagemModel(
            id=None,
            sinais_vitais=SinaisVitaisModel(
                id=None,
                pressao_arterial='115/75 mmHg',
                frequencia_cardiaca='70 bpm',
                temperatura='36.8°C',
                saturacao_oxigenio='99%',
                frequencia_respiratoria='14 rpm',
            ),
            historico_individual='enxaqueca',
            historico_familiar='enxaqueca crônica (mãe)',
            inicio_sintoma='11/11/2024',
            sintoma_localizacao='região frontal',
            sintoma='dor de cabeça',
            sintomas_associados='intensificação com movimentos rápidos da cabeça',  # noqa: E501
            escala_dor='9',
            urgencia='6',
        ),
    ),
    (
        """Durante a entrevista, o paciente se apresentou com
           dificuldade para respirar, referindo que começou em 07/11/2024,
           com sensação de aperto no peito e tosse seca associada. Ele
           classificou a dificuldade respiratória como 7 na escala de 0
           a 10. Relatou histórico de asma e rinite alérgica. Em relação
           ao histórico familiar, não há condições relevantes. A
           pressão arterial foi medida em 110/70 mmHg, com frequência
           cardíaca de 92 bpm, saturação de oxigênio em 92% e
           temperatura corporal em 37.0°C. A frequência respiratória
           foi medida em 22 respirações por minuto. A urgência foi
           classificada como 8, devido ao quadro de dificuldade
           respiratória e tosse intensa.""",
        TriagemModel(
            id=None,
            sinais_vitais=SinaisVitaisModel(
                id=None,
                pressao_arterial='110/70 mmHg',
                frequencia_cardiaca='92 bpm',
                temperatura='37.0°C',
                saturacao_oxigenio='92%',
                frequencia_respiratoria='22 rpm',
            ),
            historico_individual='asma, rinite alérgica',
            historico_familiar='nenhum relevante',
            inicio_sintoma='07/11/2024',
            sintoma_localizacao='peito',
            sintoma='dificuldade para respirar',
            sintomas_associados='tosse seca',
            escala_dor='7',
            urgencia='8',
        ),
    ),
]


class Example(TypedDict):
    input: str
    tool_calls: List[BaseModel]


def tool_example_to_messages(example: Example) -> List[BaseMessage]:
    messages: List[BaseMessage] = [HumanMessage(content=example['input'])]

    tool_calls = []
    for tool_call in example['tool_calls']:
        tool_calls.append(
            {
                'id': str(uuid.uuid4()),
                'args': tool_call.model_dump(),
                'name': tool_call.__class__.__name__,
            },
        )

    # Add the AI message with tool call results
    messages.append(AIMessage(content='', tool_calls=tool_calls))

    # Provide output for the tools, if any
    tool_outputs = example.get('tool_outputs') or [
        'You have correctly called this tool.'
    ] * len(tool_calls)

    for output, tool_call in zip(tool_outputs, tool_calls):
        messages.append(
            ToolMessage(content=output, tool_call_id=tool_call['id'])
        )
    messages.append(HumanMessage(content='Por favor, continue com a triagem.'))
    return messages
