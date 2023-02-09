from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
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
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Cartão não encontrado"},
            )
        elif cpf:
            cartoes = db.query(Cartao).filter(Cartao.cpf == cpf).all()
        else:
            cartoes = db.query(Cartao).all()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"cartoes": [cartao.to_dict() for cartao in cartoes]},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.post("/cartao", tags=["Cartao"])
def post_cartao(cartao: CartaoSchema, db: Session = Depends(get_db)):
    try:
        cartao = Cartao(**cartao.dict())
        db.add(cartao)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Cartão criado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.delete("/cartao", tags=["Cartao"])
def delete_cartao(numero: str, db: Session = Depends(get_db)):
    try:
        cartao = db.query(Cartao).filter(Cartao.numero == numero).first()
        if cartao:
            db.delete(cartao)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Cartão deletado"},
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Cartão não encontrado"},
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )

