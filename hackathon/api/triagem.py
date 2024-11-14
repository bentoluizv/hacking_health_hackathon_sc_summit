from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from hackathon.llm.chain import get_llm
from hackathon.llm.refine import (
    tool_example_to_messages,
    triagem_examples,
)
from hackathon.schemas import TriagemModel

router = APIRouter(
    prefix='/api/v1/triagem',
    tags=['Triagem'],
    dependencies=[],
)


class Input(BaseModel):
    triagem_text: str


@router.post('/', status_code=HTTPStatus.OK, response_model=TriagemModel)
def criar_nova_triagem(
    input: Input,
    llm: Annotated[ChatCohere, Depends(get_llm)],
):
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            'Você é um especialista médico responsável por '
            'extrair dados. O texto será escrito pelos '
            'profissionais de enfermagem. Sua tarefa é '
            'identificar e extrair as informações relevantes. '
            'Os sinais vitais do paciente devem ser identificados e '
            'extrair os dados conforme descrito. A pressão '
            'arterial deve ser extraída em mmHg. Exemplo: '
            '120/80. A frequência cardíaca deve ser extraída '
            'em bpm. Exemplo: 75 bpm. A temperatura corporal '
            'deve ser extraída em graus Celsius. Exemplo: '
            '37.5°C. A saturação de oxigênio deve ser extraída '
            'em porcentagem. Exemplo: 98%. A frequência '
            'respiratória deve ser extraída em rpm. Exemplo: '
            '16 rpm. Caso não seja mencionado, o valor será '
            'None. O histórico individual do paciente deve '
            'ser extraído. Inclua informações sobre doenças '
            'pré-existentes. Exemplos de doenças: diabetes, '
            'hipertensão, asma. Se não estiver presente, o '
            'valor será None. O histórico familiar deve ser '
            'extraído. Inclua doenças que afetam familiares '
            'próximos. Exemplo: câncer, mãe; hipertensão, pai. '
            'Caso não mencione histórico familiar, o valor '
            'será None. O motivo da consulta deve ser '
            'descrito. Identifique o início dos sintomas, '
            'data no formato AAAA-MM-DD. Exemplo: '
            '2024-11-10. A localização do sintoma principal '
            'deve ser extraída. Sintomas principais: dor, '
            'falta de ar, tontura, etc. Sintomas associados '
            'devem ser identificados, como febre, etc. Se essas '
            'informações não estiverem no texto, será None. Se '
            'a intensidade da dor for mencionada, extraia a '
            'escala. Exemplo: 5. Caso não mencione a escala de '
            'dor, o valor será None. A urgência do atendimento '
            'deve ser extraída. A urgência pode ser uma '
            'classificação de prioridade. Exemplo: 8. Caso a '
            'urgência não seja mencionada, o valor será None. '
            'Forneça uma extração precisa e clara das informações. '
            'Quando algum dado não for encontrado, retorne None.',
        ),
        MessagesPlaceholder('examples'),
        ('human', '{text}'),
    ])

    messages = []

    for text, tool_call in triagem_examples:
        messages.extend(
            tool_example_to_messages({
                'input': text,
                'tool_calls': [tool_call],
            })
        )

    runnable = prompt | llm.with_structured_output(schema=TriagemModel)

    output = runnable.invoke({
        'examples': messages,
        'text': input.triagem_text,
    })
    return output
