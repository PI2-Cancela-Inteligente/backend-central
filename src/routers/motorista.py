from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base, Usuario, Motorista
from pydantic import BaseModel

router = APIRouter()


Base.metadata.create_all(bind=engine)


class MotoristaSchema(BaseModel):
    telefone: str or None = None
    cpf: str
    nome: str
    matricula: str or None = None
    email: str
    senha: str or None = None

    class Config:
        orm_mode = True


@router.get("/motorista", tags=["Motorista"])
def get_motorista(cpf: str or None = None, db: Session = Depends(get_db)):
    try:
        if cpf:
            motorista = db.query(Motorista).filter(Motorista.cpf == cpf).first()
            if motorista:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "motorista": {
                            "telefone": motorista.telefone,
                            "cpf": motorista.cpf,
                            "nome": motorista.nome,
                            "id_usuario": motorista.id_usuario,
                            "matricula": motorista.matricula,
                        }
                    },
                )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Motorista não encontrado"},
            )
        else:
            motoristas = db.query(Motorista).all()
            if motoristas:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "motoristas": [
                            {
                                "telefone": motorista.telefone,
                                "cpf": motorista.cpf,
                                "nome": motorista.nome,
                                "id_usuario": motorista.id_usuario,
                                "matricula": motorista.matricula,
                            }
                            for motorista in motoristas
                        ]
                    },
                )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Nenhum motorista encontrado"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.post("/motorista", tags=["Motorista"])
def create_motorista(motorista: MotoristaSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == motorista.email).first()
    if not usuario:
        try:
            usuario = Usuario(
                email=motorista.email,
                senha=motorista.senha,
                is_admin=False,
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e)},
            )
    try:
        motorista = Motorista(
            telefone=motorista.telefone,
            cpf=motorista.cpf,
            nome=motorista.nome,
            id_usuario=usuario.id_usuario,
            matricula=motorista.matricula,
        )
        db.add(motorista)
        db.commit()
        db.refresh(motorista)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Motorista criado com sucesso",
                "motorista": {
                    "telefone": motorista.telefone,
                    "cpf": motorista.cpf,
                    "nome": motorista.nome,
                    "id_usuario": motorista.id_usuario,
                    "matricula": motorista.matricula,
                },
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.put("/motorista", tags=["Motorista"])
def update_motorista(motorista: MotoristaSchema, db: Session = Depends(get_db)):
    motorista_db = db.query(Motorista).filter(Motorista.cpf == motorista.cpf).first()
    if motorista_db:
        try:
            db.query(Motorista).filter(Motorista.cpf == motorista.cpf).update(
                {
                    "telefone": motorista.telefone,
                    "nome": motorista.nome,
                    "matricula": motorista.matricula,
                }
            )
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Motorista atualizado com sucesso"},
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e)},
            )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Motorista não encontrado"},
    )


@router.delete("/motorista", tags=["Motorista"])
def delete_motorista(cpf: str, db: Session = Depends(get_db)):
    motorista = db.query(Motorista).filter(Motorista.cpf == cpf).first()
    if motorista:
        try:
            db.delete(motorista)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Motorista deletado com sucesso"},
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(e)},
            )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Motorista não encontrado"},
    )
