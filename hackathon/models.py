from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Table,
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


sinais_vitais_por_triagem_association = Table(
    'sinais_vitais_por_triagem_association',
    Base.metadata,
    Column(
        'sinais_vitais_id', ForeignKey('sinais_vitais.id', ondelete='CASCADE')
    ),
    Column('triagem_id', ForeignKey('triagem.id', ondelete='CASCADE')),
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


class TriagemOrm(Base):
    __tablename__ = 'triagem'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, index=True, autoincrement=True
    )

    sinais_vitais_id: Mapped[int] = mapped_column(
        ForeignKey('sinais_vitais.id', use_alter=True),
    )

    sinais_vitais: Mapped[list[SinaisVitaisOrm]] = relationship(
        secondary=sinais_vitais_por_triagem_association,
        back_populates='triagem',
    )

    inicio_sintoma: Mapped[str] = mapped_column(Date)

    sintoma: Mapped[str] = mapped_column(String)

    sintoma_localizacao: Mapped[str] = mapped_column(String)

    sintomas_associados: Mapped[str] = mapped_column(String)

    historico_individual: Mapped[str] = mapped_column(String)

    historico_familiar: Mapped[str] = mapped_column(String)

    escala_dor: Mapped[str] = mapped_column(String)

    urgencia: Mapped[str] = mapped_column(String)
