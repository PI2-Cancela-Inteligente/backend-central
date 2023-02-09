from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
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
                ultimo_estacionamento.valor = ultimo_estacionamento.valor_pagar()
                db.commit()
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"message": "Estacionamento Saída Realizada"},
                )
            estaciona = Estaciona(placa=placa.placa, valor=0)
            db.add(estaciona)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Estacionamento Entrada Realizada"},
            )
        except Exception as e:

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e)},
            )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Carro não encontrado"},
    )
