from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.hash import verify_password
from database import get_db, engine
from models import Usuario, Base
from pydantic import BaseModel

router = APIRouter()

Base.metadata.create_all(bind=engine)


class UsuarioSchema(BaseModel):
    email: str
    senha: str

    class Config:
        orm_mode = True


@router.post("/login", tags=["Autenticacao"])
def login(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    try:
        usuario_query = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        if usuario:
            correct_password = verify_password(usuario.senha, usuario_query.senha)
            if not correct_password:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Senha incorreta"},
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Usuário autenticado com sucesso",
                    "usuario": {
                        "id": usuario_query.id,
                        "nome": usuario_query.nome,
                        "email": usuario_query.email,
                        "tipo": usuario_query.tipo,
                    },
                },
            )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Usuário não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro interno do servidor"},
        )