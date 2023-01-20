from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base, Carro, Motorista, Estaciona
from pydantic import BaseModel

router = APIRouter()


Base.metadata.create_all(bind=engine)


class CarroSchema(BaseModel):
    placa: str
    cor: str
    modelo: str
    marca: str
    cpf: str

    class Config:
        orm_mode = True


@router.get("/acesso-carro", tags=["Carro"])
def get_carro(placa: str or None = None, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            motorista = (
                db.query(Motorista).filter(Motorista.cpf == carro.cpf).first()
            )
            carro = carro.to_dict()
            carro["motorista_nome"] = motorista.nome
            carro["motorista_matricula"] = motorista.matricula

            estaciona = (
                db.query(Estaciona)
                .filter(Estaciona.placa == carro["placa"])
                .order_by(Estaciona.entrada.desc())
                .all()
            )
            if estaciona:
                carro["estacionamentos"] = [
                    {
                        "placa": estacionamento.placa,
                        "entrada": estacionamento.entrada,
                        "saida": estacionamento.saida,
                    }
                    for estacionamento in estaciona
                ]
            return carro
        return {"message": "Carro não encontrado"}
    except Exception as e:
        return {"message": "Erro ao buscar carro", "error": str(e)}


@router.get("/carros-motorista", tags=["Carro"])
def get_carros_motorista(
    cpf: str or None = None, db: Session = Depends(get_db)
):
    try:
        carros = db.query(Carro).filter(Carro.cpf == cpf).all()
        if carros:
            return [carro.to_dict() for carro in carros]
        return {"message": "Nenhum carro encontrado"}
    except Exception as e:
        return {"message": "Erro ao buscar carros", "error": str(e)}


@router.get("/carro", tags=["Carro"])
def get_carros(db: Session = Depends(get_db)):
    try:
        carros = db.query(Carro).all()
        if carros:
            return [carro.to_dict() for carro in carros]
        return {"message": "Nenhum carro encontrado"}
    except Exception as e:
        return {"message": "Erro ao buscar carros", "error": str(e)}


@router.post("/carro", tags=["Carro"])
def create_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    try:
        carro = Carro(**carro.dict())
        db.add(carro)
        db.commit()
        db.refresh(carro)
        return carro
    except Exception as e:
        return {"message": "Erro ao criar carro", "error": str(e)}


@router.put("/carro", tags=["Carro"])
def update_carro(
    placa: str, carro: CarroSchema, db: Session = Depends(get_db)
):
    try:
        carro = Carro(**carro.dict())
        db.query(Carro).filter(Carro.placa == placa).update(carro.to_dict())
        db.commit()
        return carro
    except Exception as e:
        return {"message": "Erro ao atualizar carro", "error": str(e)}


@router.delete("/carro", tags=["Carro"])
def delete_carro(placa: str, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            db.delete(carro)
            db.commit()
            return carro
        return {"message": "Carro não encontrado"}
    except Exception as e:
        return {"message": "Erro ao deletar carro", "error": str(e)}
