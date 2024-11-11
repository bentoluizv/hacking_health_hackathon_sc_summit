from datetime import date, datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PacienteModel(ModelConfig):
    """Informações sobre um paciente, incluindo nome e data de nascimento"""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    documento: str = Field(description='Numero do documento de identificação')

    nome: str = Field(description='Nome completo do paciente.')

    data_nascimento: date = Field(
        description='Data de nascimento do paciente no formato AAAA-MM-DD.'
    )


class SinaisVitaisModel(ModelConfig):
    """Representa os sinais vitais de um paciente, como pressão arterial,
    temperatura, frequência cardíaca e respiratória. Todos os campos são
    obrigatórios."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    pressao_arterial: str | None = Field(
        description='Pressão arterial do paciente em mmHg (ex.: 130/85).'
    )

    temperatura: str | None = Field(
        description='Temperatura corporal do paciente em °C (ex.: 37,8°C).'
    )

    frequencia_cardiaca: str | None = Field(
        description='Frequência cardíaca do paciente em bpm (ex.: 95 bpm).'
    )

    frequencia_respiratoria: str | None = Field(
        description='Frequência respiratória do paciente em rpm (ex.: 18 rpm).'
    )

    saturacao_oxigenio: str | None = Field(
        description='Saturação do oxigênio do paciente em porcentagem(ex: 97%)'
    )


class DiagnosticoModel(ModelConfig):
    """Representa o diagnóstico inicial do paciente, incluindo a condição
    principal
    diagnosticada e, se aplicável, os diagnósticos diferenciais considerados.
    """

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    condicao_principal: str | None = Field(
        description="""Nome da condição principal diagnosticada pelo médico,
        que motivou o atendimento."""
    )

    diagnostico_diferencial: list[str] | None = Field(
        description="""Lista de diagnósticos diferenciais que o médico
        considerou para a condição do paciente, caso aplicável.""",
    )


class ExameModel(ModelConfig):
    """Representa um exame solicitado durante a consulta médica, incluindo
    informações sobre o nome do exame, tipo, status, e resultado quando
    disponível."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    nome_exame: str | None = Field(
        description="""Nome do exame solicitado durante a consulta médica,
        como hemograma, ultrassonografia, entre outros. O nome descreve
        o exame ou procedimento a ser realizado para investigação da condição
         do paciente."""
    )

    data_solicitacao: datetime | None = Field(
        description="""Data e hora exatas em que o exame foi solicitado pelo
        médico, marcando o momento em que a necessidade do exame foi
        identificada
        durante o atendimento do paciente."""
    )

    tipo: str | None = Field(
        description="""Tipo de exame solicitado, por exemplo, laboratorial
         (para análises de sangue, urina),
        de imagem (como radiografia ou ultrassonografia), ou funcional (para
        testes de desempenho de órgãos ou sistemas)."""
    )

    status: str | None = Field(
        description="""Status atual do exame, representando o progresso do
        pedido,
        como 'pendente' (ainda não realizado), 'em andamento' (em execução),
        ou 'concluído' (resultado disponível ou finalizado).""",
    )

    resultado: str | None = Field(
        description="""Resultado do exame, se já disponível. Pode conter a
        descrição dos achados
        ou um resumo do diagnóstico fornecido a partir dos dados do exame,
        como valores de laboratório ou imagens resultantes.""",
    )


class MedicamentoModel(ModelConfig):
    """Representa um medicamento prescrito ao paciente, incluindo
    informações sobre o nome, dose, via de administração, frequência
    e duração do tratamento."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    nome: str | None = Field(
        description='Nome do medicamento prescrito pelo médico.'
    )

    dose: str | None = Field(
        description="""Dosagem prescrita do medicamento, incluindo a quantidade
        e a unidade de medida, como 500 mg, 10 ml, 1 comprimido, etc."""
    )

    via_administracao: str | None = Field(
        description="""Via pela qual o medicamento deve ser administrado ao
         paciente, como oral (via boca), intravenosa, subcutânea, entre outras.
         """
    )

    frequencia: str | None = Field(
        description="""Frequência com que o medicamento deve ser administrado
        ao paciente, como '8 em 8 horas', '1 vez ao dia', ou outra instrução de
        intervalo
        de tempo."""
    )

    duracao: str | None = Field(
        description="""Duração do tratamento com o medicamento, como '7 dias',
        'por 10 dias', ou outro período indicado pelo médico.""",
    )


class ProcedimentoModel(BaseModel):
    """Procedimento realizado por médico ou enfermagem que pode ser
    realizado em uma pessoa que esteja recebendo atendimento"""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso'
    )
    nome: str | None = Field(description='Nome do procedimento')
    data_solicitacao: datetime | None = Field(
        description='Data em que o procedimento foi solcitado'
    )
    tipo: str | None = Field(
        description='Tipo do procedimento que foi solicitado'
    )


class ConsultaModel(ModelConfig):
    """Dados detalhados sobre a consulta médica do paciente, incluindo
    diagnóstico, exames, medicamentos e orientações."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    data_hora: datetime | None = Field(
        description="""Data e hora exata em que a consulta foi realizada,
        indicando o início do atendimento médico."""
    )

    diagnostico_inicial: DiagnosticoModel | None = Field(
        description="""Diagnóstico inicial realizado pelo médico, contendo
        a condição principal e, se aplicável, o diagnóstico diferencial
        considerado."""
    )

    exames_solicitados: List[ExameModel] | None = Field(
        description="""Lista dos exames solicitados para confirmar o
        diagnóstico, como exames laboratoriais, de imagem ou outros
         procedimentos diagnósticos.""",
    )

    procedimentos_realizados: List[ProcedimentoModel] | None = Field(
        description="""Lista de procedimentos realizados durante a consulta,
        como intervenções específicas ou exames físicos.""",
    )

    medicamentos_prescritos: List[MedicamentoModel] | None = Field(
        description="""Lista de medicamentos prescritos, com detalhes como
         nome, dosagem, via de administração e frequência de uso.""",
    )

    orientacoes: str | None = Field(
        description="""Instruções fornecidas ao paciente sobre cuidados
        gerais, sinais de alerta e instruções de retorno ou acompanhamento."""
    )

    urgencia: int | None = Field(
        description="""Nível de urgência da condição do paciente em uma
        escala de 0 (baixa prioridade) a 10 (alta prioridade), avaliado pelo
        médico durante a consulta."""
    )


class EvolucaoEnfermagemModel(ModelConfig):
    """Registro das evoluções de enfermagem no acompanhamento do paciente
    durante o atendimento."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    data_hora: datetime | None = Field(
        description="""Data e hora exata em que a evolução foi registrada pela
        equipe de enfermagem, representando o momento do acompanhamento ou
        atualização do estado do paciente."""
    )

    resposta_ao_tratamento: str | None = Field(
        description="""Descrição detalhada de como o paciente respondeu aos
        tratamentos e intervenções realizados,
        como efeitos dos medicamentos administrados ou mudanças no quadro
        clínico após a intervenção."""
    )

    sinais_vitais: List[SinaisVitaisModel] | None = Field(
        description="""Conjunto de medições de sinais vitais registrados pela
         enfermagem durante a evolução,
        como pressão arterial, temperatura corporal, frequência cardíaca e
        respiratória, que indicam o estado clínico do paciente."""
    )

    procedimentos_realizados: List[ProcedimentoModel] | None = Field(
        description="""Lista de procedimentos de enfermagem realizados até o
        momento da evolução,
        como administração de medicamentos, coleta de exames laboratoriais ou
        de imagem, monitoramento de sintomas, entre outros."""
    )

    observacoes: str | None = Field(
        description="""Anotações adicionais sobre o estado geral do paciente,
        incluindo observações de mudanças significativas
        no quadro, recomendações de repouso ou cuidados especiais, ou qualquer
        outro detalhe relevante observado pela enfermagem."""
    )


class MotivoModel(ModelConfig):
    """Representa o motivo da consulta médica, incluindo o início dos sintomas,
    o sintoma principal, sua localização e sintomas associados."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    inicio: datetime | None = Field(
        description="""Data e hora de início dos sintomas, indicando quando o
        paciente começou a sentir o problema que motivou a consulta."""
    )

    sintoma: str | None = Field(
        description="""Sintoma principal que motivou a ida ao médico, como dor,
        febre, dificuldade para respirar, entre outros. Este sintoma é o
        principal que levou o paciente a buscar ajuda médica."""
    )

    localizacao: str | None = Field(
        description="""Localização do sintoma no corpo, como dor no peito, dor
        abdominal, sensação de falta de ar, etc. A localização deve ser
        detalhada para ajudar na avaliação do problema do paciente."""
    )

    sintomas_associados: str | None = Field(
        description="""Lista de sintomas adicionais que acompanham o sintoma
        principal, como náuseas, tontura, febre, entre outros. Cada elemento da
        lista representa um sintoma associado observado pelo paciente e/ou pelo
        profissional de saúde. Deve ser uma string com os sintomas separados
        po virgula"""
    )


class TriagemModel(ModelConfig):
    """Informações sobre o acolhimento do paciente, incluindo sinais vitais,
    histórico individual, histórico familiar, motivo da ida e escala de dor."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    sinais_vitais: list[SinaisVitaisModel] | None = Field(
        description="""
        Lista de aferições dos sinais vitais durante todo o atendimento."""
    )

    historico_individual: str | None = Field(
        description="""
        Condições médicas anteriores informadas pelo paciente.
        Deve ser uma string contento todas as condições médicas anteriores
        separados por virgula"""
    )

    historico_familiar: str | None = Field(
        description="""
        Condições médicas familiares informadas, incluindo parentesco.
        Deve ser uma string contento todas as condições médicas familiares
        separados por virgula"""
    )

    motivo: MotivoModel | None = Field(
        description="""Principal queixa informada, incluindo início dos
        sintomas, localização e sintomas associados."""
    )

    escala_dor: int | None = Field(
        description="""
        Escala de dor do paciente de 0 a 10, onde 0 é sem dor e 10 é
        dor intensa."""
    )

    urgencia: int | None = Field(
        description="""Urgência do atendimento em uma escala de 0 a 10, onde 0
        é pouco urgente e 10 é prioridade máxima."""
    )


class AtendimentoModel(ModelConfig):
    """Dados centralizados sobre o atendimento do paciente, incluindo data,
    informações do paciente, triagem, consulta e evolução da enfermagem."""

    id: int | None = Field(
        description='Id gerado pelo banco de dados ao criar o recurso',
        default=None,
    )

    data: datetime = Field(
        description="""Data e hora da realização do atendimento, padrão é a
        data atual (datetime.now).""",
    )

    paciente: PacienteModel = Field(
        description="""Dados pessoais e históricos do paciente atendido."""
    )

    triagem: TriagemModel | None = Field(
        description="""Informações obtidas na triagem, como sinais vitais e
        motivos para o atendimento.""",
    )

    consultas: list[ConsultaModel] | None = Field(
        description="""Informações da consulta médica, incluindo diagnósticos e
        prescrições.""",
    )

    evolucoes: list[EvolucaoEnfermagemModel] | None = Field(
        description="""Registro da evolução da enfermagem, com detalhes sobre
         intervenções e observações ao longo do atendimento.""",
    )
