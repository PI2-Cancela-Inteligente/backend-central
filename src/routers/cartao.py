from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base, Cartao
from pydantic import BaseModel

router = APIRouter()


Base.metadata.create_all(bind=engine)


class CartaoSchema(BaseModel):
    numero: str
    nome: str
    validade: str
    cvv: str
    id_usuario: int
    cpf: str

    class Config:
        orm_mode = True


@router.get("/cartao", tags=["Cartao"])
def get_cartao(
    numero: str or None = None,
    cpf: str or None = None,
    db: Session = Depends(get_db),
):
    try:
        if numero:
            cartao = db.query(Cartao).filter(Cartao.numero == numero).first()
            if cartao:
                return cartao.to_dict()
            return Response(
                status_code=404, content={"message": "Cartão não encontrado"}
            )
        elif cpf:
            cartoes = db.query(Cartao).filter(Cartao.cpf == cpf).all()
        else:
            cartoes = db.query(Cartao).all()
        return Response(
            status_code=200,
            content={"cartoes": [cartao.to_dict() for cartao in cartoes]},
        )
    except Exception as e:
        return Response(status_code=500, content={"message": str(e)})


@router.post("/cartao", tags=["Cartao"])
def post_cartao(cartao: CartaoSchema, db: Session = Depends(get_db)):
    try:
        cartao = Cartao(**cartao.dict())
        db.add(cartao)
        db.commit()
        return Response(status_code=201, content={"message": "Cartão criado"})
    except Exception as e:
        return Response(status_code=500, content={"message": str(e)})


@router.delete("/cartao", tags=["Cartao"])
def delete_cartao(numero: str, db: Session = Depends(get_db)):
    try:
        cartao = db.query(Cartao).filter(Cartao.numero == numero).first()
        if cartao:
            db.delete(cartao)
            db.commit()
            return Response(
                status_code=200, content={"message": "Cartão deletado"}
            )
        return Response(
            status_code=404, content={"message": "Cartão não encontrado"}
        )
    except Exception as e:
        return Response(status_code=500, content={"message": str(e)})
