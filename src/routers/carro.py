from typing import Union
from fastapi import APIRouter, Depends, status, Request

# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from src.schemas.placa_carro import PlacaCarro

from sqlalchemy.orm import Session

from src.database import get_db, engine
from src.models import Base, Carro, Motorista

router = APIRouter()


Base.metadata.create_all(bind=engine)


@router.get("/carro", tags=["Carro"])
def get_carro(placa: str or None = None, db: Session = Depends(get_db)):
    try:
        carro = db.query(Carro).filter(Carro.placa == placa).first()
        if carro:
            motorista = (
                db.query(Motorista)
                .filter(Motorista.id == carro.motorista_id)
                .first()
            )
            carro = carro.to_dict()
            carro["motorista_nome"] = motorista.nome
            carro["motorista_matricula"] = motorista.matricula
            return carro
        return {"message": "Carro não encontrado"}
    except Exception as e:
        return {"message": "Erro ao buscar carro", "error": str(e)}
