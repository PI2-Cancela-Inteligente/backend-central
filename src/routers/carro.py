from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
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


@router.get("/historico-carro", tags=["Carro"])
def get_carro(placa: str or None = None, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            motorista = db.query(Motorista).filter(Motorista.cpf == carro.cpf).first()
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
                        "entrada": estacionamento.entrada.strftime("%d/%m/%Y %H:%M:%S"),
                        "saida": estacionamento.saida.strftime("%d/%m/%Y %H:%M:%S")
                        if estacionamento.saida
                        else None,
                        "valor": str(estacionamento.valor),
                    }
                    for estacionamento in estaciona
                ]
            return JSONResponse(status_code=status.HTTP_200_OK, content=carro)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Carro não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.get("/carro", tags=["Carro"])
def get_carros(cpf: str or None = None, db: Session = Depends(get_db)):
    try:
        if cpf:
            carros = db.query(Carro).filter(Carro.cpf == cpf).all()
        else:
            carros = db.query(Carro).all()
        if carros:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[carro.to_dict() for carro in carros],
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Nenhum carro encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.post("/carro", tags=["Carro"])
def create_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    try:
        carro = Carro(**carro.dict())
        db.add(carro)
        db.commit()
        db.refresh(carro)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=carro.to_dict()
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar carro", "error": str(e)},
        )


@router.put("/carro", tags=["Carro"])
def update_carro(placa: str, carro: CarroSchema, db: Session = Depends(get_db)):
    carro_db = db.query(Carro).filter(Carro.placa == placa).first()
    if not carro_db:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Carro não encontrado"},
        )
    try:
        carro = Carro(**carro.dict())
        db.query(Carro).filter(Carro.placa == placa).update(carro.to_dict())
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=carro.to_dict())
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao atualizar carro",
                "error": str(e),
            },
        )


@router.delete("/carro", tags=["Carro"])
def delete_carro(placa: str, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            db.delete(carro)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Carro deletado", "carro": carro.to_dict()},
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Carro não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao deletar carro", "error": str(e)},
        )
