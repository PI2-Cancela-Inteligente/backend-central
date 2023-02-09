from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.hash import verify_password, create_access_token
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
            access_token = create_access_token(data={"sub": usuario.email})
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Login realizado com sucesso",
                    "token": access_token,
                },
            )
            response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
            )
            return response
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Usuário não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro interno do servidor"},
        )
