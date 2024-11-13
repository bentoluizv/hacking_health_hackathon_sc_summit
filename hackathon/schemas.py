from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SinaisVitaisModel(BaseModel):
    """
    Representa os sinais vitais de um paciente, que são medições
    essenciais para avaliar o estado de saúde do paciente durante
    o atendimento médico. Esses dados fornecem informações cruciais
    sobre o funcionamento do corpo e podem indicar possíveis condições
    médicas, como infecções, problemas respiratórios ou cardiovasculares.
    Cada campo é opcional e pode ser 'None' caso a informação não
    esteja disponível ou não tenha sido registrada.

    Exemplos de sinais vitais:
    - pressao_arterial: A pressão arterial é medida em milímetros
      de mercúrio (mmHg) e indica a força que o sangue exerce
      sobre as paredes das artérias. Ela é dividida em dois valores:
      a pressão sistólica (máxima) e a diastólica (mínima). Exemplo:
      '120/80'.
    - temperatura: A temperatura corporal é um indicador de infecção
      ou inflamação. Exemplo de entrada: '37.5°C' pode indicar febre
      leve.
    - frequencia_cardiaca: A frequência cardíaca indica o número de
      batimentos do coração por minuto (bpm). Um valor normal para
      adultos em repouso é entre 60 e 100 bpm. Exemplo: '72 bpm' está
      dentro do intervalo considerado normal.
    - frequencia_respiratoria: A frequência respiratória indica o
      número de respirações realizadas por minuto. O valor normal é
      entre 12 e 20 respirações por minuto em adultos em repouso.
      Exemplo: '16 rpm' indica uma respiração normal.
    - saturacao_oxigenio: A saturação de oxigênio no sangue, medida
      em porcentagem. Exemplo: '98%' é normal, enquanto valores
      abaixo de 90% podem indicar insuficiência respiratória grave.
    """

    id: Optional[int] = Field(
        None,
        description="""ID gerado automaticamente ao registrar o recurso
        no sistema de triagem, normalmente atribuído pelo banco de dados
        do hospital.""",
    )

    pressao_arterial: Optional[str] = Field(
        None,
        description="""Pressão arterial medida em milímetros de mercúrio
        (mmHg). O formato esperado é 'sistólica/diastólica'. Exemplo:
        '120/80'. Se a pressão sistólica for superior a 140 ou a diastólica
        superior a 90, pode indicar hipertensão e exigir atenção imediata.""",
    )

    temperatura: Optional[str] = Field(
        None,
        description="""Temperatura corporal medida em graus Celsius (°C).
        Uma temperatura acima de 37.5°C pode indicar febre e possível
        infecção. Exemplo de entrada: '38.0°C'.""",
    )

    frequencia_cardiaca: Optional[str] = Field(
        None,
        description="""Frequência cardíaca medida em batimentos por minuto
        (bpm). Para um adulto em repouso, valores normais variam entre
        60 e 100 bpm. Exemplo: '72 bpm' é considerado normal, enquanto
        uma frequência cardíaca inferior a 60 bpm (bradicardia) ou superior
        a 100 bpm (taquicardia) pode indicar problemas de saúde.""",
    )

    frequencia_respiratoria: Optional[str] = Field(
        None,
        description="""Frequência respiratória medida em respirações por
        minuto (rpm). A frequência normal para um adulto é entre 12 e 20
        rpm. Exemplo: '18 rpm' indica respiração normal. Frequências fora
        dessa faixa podem indicar dificuldades respiratórias.""",
    )

    saturacao_oxigenio: Optional[str] = Field(
        None,
        description="""Saturação de oxigênio no sangue, medida em porcentagem.
        Um valor normal é entre 95% e 100%. Saturações abaixo de 90% podem
        indicar insuficiência respiratória grave e requerem atenção imediata.
        Exemplo: '98%'.""",
    )


class TriagemModel(ModelConfig):
    """
    Representa o processo de triagem médica, onde um paciente fornece
    informações sobre seus sinais vitais, histórico médico e familiar,
    e o motivo da consulta. Esse processo é fundamental para determinar
    a gravidade da condição do paciente e priorizar o atendimento com
    base na urgência da situação.

    Campos:
    - sinais_vitais: Contém informações sobre pressão arterial, temperatura,
      frequência cardíaca, frequência respiratória e saturação de oxigênio.
    - historico_individual: Informações sobre doenças ou condições
      pré-existentes, como hipertensão, diabetes, etc. Exemplos de entrada:
      'hipertensão, diabetes tipo 2'.
    - historico_familiar: Informações sobre doenças comuns na família, como
      câncer, doenças cardíacas, etc. Exemplo: 'câncer, mãe; hipertensão, pai'.
    - motivo: Motivo da consulta, incluindo sintoma principal, data de início
      dos sintomas, localização do sintoma no corpo e sintomas associados.
    - escala_dor: Avaliação da dor que o paciente está sentindo em uma escala
      de 0 a 10, onde 0 significa 'sem dor' e 10 significa 'dor intensa'.
      Isso ajuda os profissionais de saúde a determinar a necessidade de
      controle imediato da dor. Exemplo: '9'.
    - urgencia: Nível de urgência do atendimento, de 0 a 10, sendo 0 pouco
      urgente e 10 extremamente urgente. Esse campo é usado para classificar
      a prioridade do atendimento. Exemplo: '10' é uma situação de emergência.
    """

    id: Optional[int] = Field(
        None,
        description="""ID único gerado automaticamente ao registrar a triagem
        no sistema do hospital, usado para controle e acompanhamento do
        atendimento.""",
    )

    sinais_vitais: Optional[SinaisVitaisModel] = Field(
        None,
        description="""Sinais vitais do paciente, como pressão arterial,
        temperatura, frequência cardíaca, frequência respiratória e saturação
        de oxigênio, que fornecem informações sobre o estado de saúde do
          paciente.""",
    )

    historico_individual: Optional[str] = Field(
        None,
        description="""Histórico médico do paciente, incluindo condições
        pré-existentes como doenças cardiovasculares, diabetes, problemas
        respiratórios, entre outros. Exemplo: 'hipertensão, diabetes tipo 2'.
        """,
    )

    historico_familiar: Optional[str] = Field(
        None,
        description="""Histórico médico da família, incluindo doenças
        prevalentes em parentes próximos, como câncer, doenças cardíacas,
        diabetes, etc. Exemplo: 'câncer, mãe; hipertensão, pai'.""",
    )

    inicio_sintoma: Optional[str] = Field(
        None,
        description="""Data e hora de início dos sintomas. Pode ser uma data
        exata ou uma estimativa. Exemplo: 'há 2 horas', 'ontem à noite', ou
        'início há 3 dias'. Sempre que possível, converta para o formato
        AAAA-MM-DD. Esse campo ajuda a entender a evolução dos sintomas.""",
    )

    sintoma: Optional[str] = Field(
        None,
        description="""Sintoma principal que levou o paciente a procurar
        atendimento médico. Pode ser algo como 'dor no peito', 'dificuldade
        para respirar', 'febre intensa', etc. Este campo é crucial para
        direcionar o profissional de saúde ao diagnóstico adequado.""",
    )

    sintoma_localizacao: Optional[str] = Field(
        None,
        description="""Localização do sintoma no corpo. Especificar a área
        ou parte do corpo onde o paciente sente o sintoma. Exemplos incluem:
        'dor no peito', 'dificuldade para respirar no peito', 'dor abdominal
        no lado esquerdo'.""",
    )

    sintomas_associados: Optional[str] = Field(
        None,
        description="""Sintomas adicionais que acompanham o sintoma principal,
        como náuseas, tontura, calafrios, etc. Devem ser listados separadamente
        por vírgulas. Exemplo: 'febre, calafrios, tontura'.""",
    )

    escala_dor: Optional[str] = Field(
        None,
        description="""Avaliação da intensidade da dor que o paciente está
        sentindo, com base numa escala de 0 a 10, onde 0 significa 'sem dor'
        e 10 significa 'dor intensa'. Essencial para decidir sobre a
        necessidade de alívio imediato da dor. Exemplo: '9'.""",
    )

    urgencia: Optional[str] = Field(
        None,
        description="""Nível de urgência do atendimento médico, de 0 a 10.
        Um valor de 10 indica uma condição crítica que exige atenção
        imediata, enquanto 0 indica uma situação sem urgência. Exemplo:
        '10' é uma emergência médica. Deve ser transformado em número""",
    )
