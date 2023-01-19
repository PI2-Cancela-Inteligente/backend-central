from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from datetime import datetime
from src.database import get_db, engine
from src.models import Base, Estaciona, Carro

router = APIRouter()


Base.metadata.create_all(bind=engine)


@router.post("/estaciona", tags=["Estaciona"])
def post_estaciona(placa: str, db: Session = Depends(get_db)):
    carro = db.query(Carro).filter(Carro.placa == placa).first()
    if carro:
        try:
            ultimo_estacionamento = (
                db.query(Estaciona)
                .filter(Estaciona.placa == placa)
                .order_by(Estaciona.entrada.desc())
                .first()
            )
            if ultimo_estacionamento and ultimo_estacionamento.saida is None:
                ultimo_estacionamento.saida = datetime.now()
                db.commit()
                return {"message": "Estacionamento Saída Realizada"}
            estaciona = Estaciona(placa=placa)
            db.add(estaciona)
            db.commit()
            return {"message": "Estacionamento Entrada Registrada"}
        except Exception as e:
            return {
                "message": "Erro ao registrar estacionamento",
                "error": str(e),
            }
    return {"message": "Carro não encontrado"}
