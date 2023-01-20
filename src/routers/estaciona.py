from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, engine
from models import Base, Estaciona, Carro
from pydantic import BaseModel

router = APIRouter()


Base.metadata.create_all(bind=engine)


class EstacionaSchema(BaseModel):
    placa: str

    class Config:
        orm_mode = True


@router.post("/estaciona", tags=["Estaciona"])
def post_estaciona(placa: EstacionaSchema, db: Session = Depends(get_db)):
    carro = db.query(Carro).filter(Carro.placa == placa.placa).first()
    if carro:
        try:
            ultimo_estacionamento = (
                db.query(Estaciona)
                .filter(Estaciona.placa == placa.placa)
                .order_by(Estaciona.entrada.desc())
                .first()
            )
            if ultimo_estacionamento and ultimo_estacionamento.saida is None:
                ultimo_estacionamento.saida = datetime.now()
                db.commit()
                return {"message": "Estacionamento Saída Realizada"}
            estaciona = Estaciona(placa=placa.placa)
            db.add(estaciona)
            db.commit()
            return {"message": "Estacionamento Entrada Registrada"}
        except Exception as e:
            return {
                "message": "Erro ao registrar estacionamento",
                "error": str(e),
            }
    return {"message": "Carro não encontrado"}
