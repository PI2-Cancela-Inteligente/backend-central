from sqlalchemy import TIMESTAMP, Column, String, BigInteger, ForeignKey

from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "usuario"

    id_usuario = Column(BigInteger, primary_key=True, Nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)


class Admin(Base):
    __tablename__ = "admin"

    id_admin = Column(BigInteger, primary_key=True, nullable=False)
    id_usuario = Column(
        BigInteger, ForeignKey("usuario.id_usuario"), nullable=False
    )


class Motorista(Base):
    __tablename__ = "motorista"

    telefone = Column(String(100), nullable=False)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(15), nullable=False, primary_key=True)
    id_usuario = Column(
        BigInteger,
        ForeignKey("usuario.id_usuario"),
        nullable=False,
        primary_key=True,
    )
    matricula = Column(String(50), nullable=False)


class Carro(Base):
    __tablename__ = "carro"

    placa = Column(String(50), nullable=False, primary_key=True)
    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    cor = Column(String(50), nullable=False)
    motorista_cpf = Column(
        String(15), ForeignKey("motorista.cpf"), nullable=False
    )
    usuario_id = Column(
        BigInteger, ForeignKey("usuario.id_usuario"), nullable=False
    )


class Estaciona(Base):
    __tablename__ = "estaciona"

    placa = Column(
        String(50), ForeignKey("carro.placa"), nullable=False, primary_key=True
    )
    entrada = Column(
        TIMESTAMP,
        nullable=False,
        primary_key=True,
        server_default=func.current_timestamp(),
    )
    saida = Column(TIMESTAMP, nullable=False)
