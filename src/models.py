from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
    BigInteger,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(BigInteger, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(500), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    motorista = relationship(
        "Motorista",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Motorista(Base):
    __tablename__ = "motorista"
    telefone = Column(String(20), nullable=True)
    cpf = Column(String(15), nullable=False, primary_key=True)
    nome = Column(String(200), nullable=False)
    id_usuario = Column(
        BigInteger,
        ForeignKey("usuario.id_usuario"),
        nullable=False,
        primary_key=True,
    )
    matricula = Column(String(50), unique=True)
    usuario = relationship("Usuario", back_populates="motorista")


class Carro(Base):
    __tablename__ = "carro"
    placa = Column(String(50), primary_key=True)
    cor = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    cpf = Column(String(15), nullable=False)
    id_usuario = Column(BigInteger, nullable=False)
    motorista = relationship(
        "Motorista",
        back_populates="carro",
        primaryjoin="and_(Motorista.cpf == Carro.cpf, Motorista.id_usuario == Carro.id_usuario)",  # noqa E501
    )


class Estaciona(Base):
    __tablename__ = "estaciona"
    placa = Column(String(50), nullable=False, primary_key=True)
    entrada = Column(
        TIMESTAMP,
        nullable=False,
        primary_key=True,
        server_default=func.current_timestamp(),
    )
    saida = Column(TIMESTAMP)
