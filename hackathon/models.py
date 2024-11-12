from datetime import date, datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


evolucao_procedimentos_association = Table(
    'evolucao_procedimentos_association',
    Base.metadata,
    Column(
        'evolucao_enfermagem_id',
        ForeignKey('evolucao_enfermagem.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'procedimento_id',
        ForeignKey('procedimento.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)


consulta_procedimentos_association = Table(
    'consulta_procedimentos_association',
    Base.metadata,
    Column(
        'consulta_id',
        ForeignKey('consulta.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'procedimento_id',
        ForeignKey('procedimento.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)

consulta_medicamentos_association = Table(
    'consulta_medicamentos_association',
    Base.metadata,
    Column(
        'consulta_id',
        ForeignKey('consulta.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'medicamento_id',
        ForeignKey('medicamento.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)


consulta_exame_association = Table(
    'consulta_exame_association',
    Base.metadata,
    Column(
        'consulta_id',
        ForeignKey('consulta.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'exame_id',
        ForeignKey('exame.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)

sinais_vitais_por_triagem_association = Table(
    'sinais_vitais_por_triagem_association',
    Base.metadata,
    Column(
        'sinais_vitais_id', ForeignKey('sinais_vitais.id', ondelete='CASCADE')
    ),
    Column('triagem_id', ForeignKey('triagem.id', ondelete='CASCADE')),
)


sinais_vitais_por_evolucao_association = Table(
    'sinais_vitais_por_evolucao_association',
    Base.metadata,
    Column(
        'sinais_vitais_id', ForeignKey('sinais_vitais.id', ondelete='CASCADE')
    ),
    Column(
        'evolucao_enfermagem_id',
        ForeignKey('evolucao_enfermagem.id', ondelete='CASCADE'),
    ),
)


class SinaisVitaisOrm(Base):
    __tablename__ = 'sinais_vitais'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    pressao_arterial: Mapped[str] = mapped_column(String)

    temperatura: Mapped[str] = mapped_column(String)

    frequencia_cardiaca: Mapped[str] = mapped_column(String)

    frequencia_respiratoria: Mapped[str] = mapped_column(String)

    saturacao_oxigenio: Mapped[str] = mapped_column(String)

    triagem: Mapped[list['TriagemOrm']] = relationship(
        secondary=sinais_vitais_por_triagem_association,
        back_populates='sinais_vitais',
    )

    evolucao_enfermagem: Mapped[list['EvolucaoEnfermagemOrm']] = relationship(
        secondary=sinais_vitais_por_evolucao_association,
        back_populates='sinais_vitais',
    )


class TriagemOrm(Base):
    __tablename__ = 'triagem'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, index=True, autoincrement=True
    )

    atendimento_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('atendimento.id', use_alter=True),
        nullable=False,
    )

    atendimento: Mapped['AtendimentoOrm'] = relationship(
        back_populates='triagem'
    )

    sinais_vitais_id: Mapped[int] = mapped_column(
        ForeignKey('sinais_vitais.id', use_alter=True),
    )

    sinais_vitais: Mapped[list[SinaisVitaisOrm]] = relationship(
        secondary=sinais_vitais_por_triagem_association,
        back_populates='triagem',
    )

    historico_individual: Mapped[str] = mapped_column(String)

    historico_familiar: Mapped[str] = mapped_column(String)

    escala_dor: Mapped[int] = mapped_column(Integer)

    urgencia: Mapped[int] = mapped_column(Integer)

    motivo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('motivo.id', use_alter=True),
        nullable=False,
    )

    motivo: Mapped['MotivoOrm'] = relationship(
        'MotivoOrm',
        back_populates='triagens',
        foreign_keys=[motivo_id],
    )


class AtendimentoOrm(Base):
    __tablename__ = 'atendimento'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, index=True, autoincrement=True
    )

    paciente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('paciente.id', use_alter=True), nullable=False
    )

    paciente: Mapped['PacienteOrm'] = relationship(
        back_populates='atendimentos',
        uselist=False,
        lazy='joined',
    )

    triagem: Mapped['TriagemOrm'] = relationship(
        back_populates='atendimento', uselist=False, default=None
    )

    evolucoes: Mapped[list['EvolucaoEnfermagemOrm']] = relationship(
        'EvolucaoEnfermagemOrm',
        back_populates='atendimento',
        default_factory=list,
    )

    consultas: Mapped[list['ConsultaOrm']] = relationship(
        back_populates='atendimento', default_factory=list
    )

    data: Mapped[datetime] = mapped_column(default_factory=func.now)


class DiagnosticoOrm(Base):
    __tablename__ = 'diagnostico'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    condicao_principal: Mapped[str]

    diagnostico_diferencial: Mapped[str]

    consulta_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('consulta.id', use_alter=True),
        unique=True,
        nullable=False,
    )

    consulta: Mapped['ConsultaOrm'] = relationship(
        'ConsultaOrm',
        back_populates='diagnostico',
        uselist=False,
    )


class StatusExame(PyEnum):
    pendente = 'pendente'
    em_andamento = 'em andamento'
    concluido = 'concluído'


class ExameOrm(Base):
    __tablename__ = 'exame'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(String)

    data_solicitacao: Mapped[datetime] = mapped_column(DateTime)

    tipo: Mapped[str] = mapped_column(String)

    resultado: Mapped[str] = mapped_column(Text, nullable=True)

    consultas: Mapped[list['ConsultaOrm']] = relationship(
        secondary=consulta_exame_association,
        primaryjoin='ExameOrm.id == consulta_exame_association.c.exame_id',
        secondaryjoin='ConsultaOrm.id == consulta_exame_association.c.consulta_id',  # noqa: E501
        back_populates='exames_solicitados',
    )

    status: Mapped[StatusExame] = mapped_column(
        Enum(StatusExame), default=StatusExame.pendente
    )


class ProcedimentoOrm(Base):
    __tablename__ = 'procedimento'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String)

    data_solicitacao: Mapped[datetime] = mapped_column(DateTime)

    tipo: Mapped[str] = mapped_column(String)

    consultas: Mapped[list['ConsultaOrm']] = relationship(
        'ConsultaOrm',
        secondary=consulta_procedimentos_association,
        primaryjoin='ProcedimentoOrm.id == consulta_procedimentos_association.c.procedimento_id',  # noqa: E501
        secondaryjoin='ConsultaOrm.id == consulta_procedimentos_association.c.consulta_id',  # noqa: E501
        back_populates='procedimentos_realizados',
    )

    evolucoes: Mapped[list['EvolucaoEnfermagemOrm']] = relationship(
        secondary=evolucao_procedimentos_association,
        back_populates='procedimentos_realizados',
    )


class ConsultaOrm(Base):
    __tablename__ = 'consulta'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    atendimento_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('atendimento.id', use_alter=True), nullable=False
    )

    atendimento: Mapped['AtendimentoOrm'] = relationship(
        back_populates='consultas'
    )

    data_hora: Mapped[datetime] = mapped_column(DateTime)

    diagnostico: Mapped[DiagnosticoOrm] = relationship(
        'DiagnosticoOrm',
        back_populates='consulta',
        uselist=False,
    )

    orientacoes: Mapped[Optional[str]] = mapped_column(Text)

    urgencia: Mapped[int] = mapped_column(Integer)

    exames_solicitados: Mapped[list[ExameOrm]] = relationship(
        secondary=consulta_exame_association,
        back_populates='consultas',
        primaryjoin='ConsultaOrm.id == consulta_exame_association.c.consulta_id',  # noqa: E501
        secondaryjoin='ExameOrm.id == consulta_exame_association.c.exame_id',
        default_factory=list,
    )

    procedimentos_realizados: Mapped[list['ProcedimentoOrm']] = relationship(
        secondary=consulta_procedimentos_association,
        primaryjoin='ConsultaOrm.id == consulta_procedimentos_association.c.consulta_id',  # noqa: E501
        secondaryjoin='ProcedimentoOrm.id == consulta_procedimentos_association.c.procedimento_id',  # noqa: E501
        back_populates='consultas',
        default_factory=list,
    )

    medicamentos_prescritos: Mapped[list['MedicamentoOrm']] = relationship(
        secondary=consulta_medicamentos_association,
        back_populates='consultas',
        default_factory=list,
    )


class PacienteOrm(Base):
    __tablename__ = 'paciente'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    documento: Mapped[str] = mapped_column(String, unique=True, index=True)

    nome: Mapped[str] = mapped_column(String, index=True)

    data_nascimento: Mapped[date] = mapped_column(Date)

    atendimentos: Mapped[list['AtendimentoOrm']] = relationship(
        back_populates='paciente',
        default_factory=list,
    )


class MotivoOrm(Base):
    __tablename__ = 'motivo'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    inicio: Mapped[datetime] = mapped_column(DateTime)

    sintoma: Mapped[str] = mapped_column(String)

    localizacao: Mapped[str] = mapped_column(String)

    sintomas_associados: Mapped[str] = mapped_column(String)

    triagens: Mapped[list['TriagemOrm']] = relationship(
        'TriagemOrm',
        back_populates='motivo',
    )


class MedicamentoOrm(Base):
    __tablename__ = 'medicamento'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )
    atendimento: Mapped[int] = mapped_column(
        Integer, ForeignKey('atendimento.id', use_alter=True), nullable=False
    )

    nome: Mapped[str]

    dose: Mapped[str]

    via_administracao: Mapped[str]

    frequencia: Mapped[str]

    duracao: Mapped[str] = mapped_column(String)

    consultas: Mapped[list['ConsultaOrm']] = relationship(
        secondary=consulta_medicamentos_association,
        back_populates='medicamentos_prescritos',
    )


class EvolucaoEnfermagemOrm(Base):
    __tablename__ = 'evolucao_enfermagem'

    id: Mapped[int] = mapped_column(
        Integer,
        init=False,
        primary_key=True,
        index=True,
    )

    atendimento_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('atendimento.id', use_alter=True), nullable=False
    )

    atendimento: Mapped['AtendimentoOrm'] = relationship(
        'AtendimentoOrm',
        back_populates='evolucoes',
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime, default_factory=func.now
    )

    resposta_ao_tratamento: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    sinais_vitais: Mapped[list[SinaisVitaisOrm]] = relationship(
        secondary=sinais_vitais_por_evolucao_association,
        back_populates='evolucao_enfermagem',
        default_factory=list,
    )

    procedimentos_realizados: Mapped[list['ProcedimentoOrm']] = relationship(
        secondary=evolucao_procedimentos_association,
        back_populates='evolucoes',
        default_factory=list,
    )
