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

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "email": self.email,
            "senha": self.senha,
            "is_admin": self.is_admin,
        }


class Motorista(Base):
    __tablename__ = "motorista"
    cpf = Column(String(15), nullable=False, primary_key=True)
    telefone = Column(String(20), nullable=True)
    nome = Column(String(200), nullable=False)
    id_usuario = Column(
        BigInteger,
        ForeignKey("usuario.id_usuario"),
        nullable=False,
        unique=True,
    )
    matricula = Column(String(50), unique=True)
    usuario = relationship("Usuario", back_populates="motorista")
    carros = relationship(
        "Carro",
        back_populates="motorista",
        cascade="all, delete-orphan",
    )


class Carro(Base):
    __tablename__ = "carro"
    placa = Column(String(50), primary_key=True)
    cor = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    cpf = Column(
        String(15),
        ForeignKey("motorista.cpf"),
        nullable=False,
    )
    motorista = relationship(
        "Motorista",
        back_populates="carros",
        uselist=False,
    )

    def to_dict(self):
        return {
            "placa": self.placa,
            "cor": self.cor,
            "modelo": self.modelo,
            "marca": self.marca,
            "cpf": self.cpf,
        }


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
