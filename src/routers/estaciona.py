from fastapi import APIRouter, Depends, Response

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
                ultimo_estacionamento.valor = (
                    ultimo_estacionamento.valor_pagar()
                )
                db.commit()
                return Response(
                    status_code=201,
                    content={"message": "Estacionamento Saída Realizada"},
                )
            estaciona = Estaciona(placa=placa.placa)
            db.add(estaciona)
            db.commit()

            return Response(
                status_code=201,
                content={"message": "Estacionamento Entrada Realizada"},
            )
        except Exception as e:
            return {
                "message": "Erro ao registrar estacionamento",
                "error": str(e),
            }
    # return 404 if car not found
    return Response(
        status_code=404, content={"message": "Carro não encontrado"}
    )
