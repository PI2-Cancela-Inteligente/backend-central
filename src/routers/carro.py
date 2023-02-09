from fastapi import APIRouter, Depends, Response

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


@router.get("/historico-carro", tags=["Carro"])
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
            return Response(status_code=200, content=carro)
        return Response(
            status_code=404, content={"message": "Carro não encontrado"}
        )
    except Exception as e:
        return Response(status_code=500, content={"message": str(e)})


@router.get("/carros-motorista", tags=["Carro"])
def get_carros_motorista(
    cpf: str or None = None, db: Session = Depends(get_db)
):
    try:
        carros = db.query(Carro).filter(Carro.cpf == cpf).all()
        if carros:
            return Response(
                status_code=200, content=[carro.to_dict() for carro in carros]
            )
        return Response(
            status_code=404, content={"message": "Nenhum carro encontrado"}
        )

    except Exception as e:
        return Response(status_code=500, content={"message": str(e)})


@router.get("/carro", tags=["Carro"])
def get_carros(response: Response, db: Session = Depends(get_db)):
    try:
        carros = db.query(Carro).all()
        if carros:
            response.status_code = 200
            return {"carros": [carro.to_dict() for carro in carros]}
        response.status_code = 404
        return {"message": "Nenhum carro encontrado"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


@router.post("/carro", tags=["Carro"])
def create_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    try:
        carro = Carro(**carro.dict())
        db.add(carro)
        db.commit()
        db.refresh(carro)
        return Response(status_code=201, content=carro.to_dict())
    except Exception as e:
        return Response(
            status_code=500,
            content={"message": "Erro ao criar carro", "error": str(e)},
        )


@router.put("/carro", tags=["Carro"])
def update_carro(
    placa: str, carro: CarroSchema, db: Session = Depends(get_db)
):
    try:
        carro = Carro(**carro.dict())
        db.query(Carro).filter(Carro.placa == placa).update(carro.to_dict())
        db.commit()
        return Response(status_code=200, content=carro.to_dict())
    except Exception as e:
        return Response(
            status_code=500,
            content=Response(
                status_code=500,
                content={
                    "message": "Erro ao atualizar carro",
                    "error": str(e),
                },
            ),
        )


@router.delete("/carro", tags=["Carro"])
def delete_carro(placa: str, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            db.delete(carro)
            db.commit()
            return Response(
                status_code=200,
                content={
                    "message": "Carro deletado",
                    "carro": carro.to_dict(),
                },
            )
        return Response(
            status_code=404, content={"message": "Carro não encontrado"}
        )
    except Exception as e:
        return Response(
            status_code=500,
            content={"message": "Erro ao deletar carro", "error": str(e)},
        )
