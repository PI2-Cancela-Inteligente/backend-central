from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.hash import create_password_hash
from database import get_db, engine
from models import Base, Usuario
from pydantic import BaseModel

router = APIRouter()


Base.metadata.create_all(bind=engine)


class UsuarioSchema(BaseModel):
    email: str
    senha: str or None = None
    is_admin: bool

    class Config:
        orm_mode = True


@router.get("/usuario", tags=["Usuario"])
def get_usuarios(id_usuario: str or None = None, db: Session = Depends(get_db)):
    try:
        if id_usuario:
            usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
            if usuario:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "usuario": {
                            "id_usuario": usuario.id_usuario,
                            "email": usuario.email,
                            "is_admin": usuario.is_admin,
                        }
                    },
                )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Usuario não encontrado"},
            )

        usuarios = db.query(Usuario).all()
        if usuarios:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "usuarios": [
                        {
                            "id_usuario": usuario.id_usuario,
                            "email": usuario.email,
                            "is_admin": usuario.is_admin,
                        }
                        for usuario in usuarios
                    ]
                },
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Nenhum usuario encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.post("/usuario", tags=["Usuario"])
def create_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    try:
        usuario_existe = (
            db.query(Usuario).filter(Usuario.email == usuario.email).first()
        )
        if usuario_existe:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email já cadastrado"},
            )
        usuario.senha = create_password_hash(usuario.senha)
        usuario = Usuario(**usuario.dict())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Usuario criado com sucesso",
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "email": usuario.email,
                    "is_admin": usuario.is_admin,
                },
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar usuario", "error": str(e)},
        )


@router.put("/usuario", tags=["Usuario"])
def update_usuario(
    id_usuario: int,
    usuarioSchema: UsuarioSchema,
    db: Session = Depends(get_db),
):
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            usuario.email = usuarioSchema.email
            if usuarioSchema.senha:
                usuario.senha = create_password_hash(usuarioSchema.senha)
            usuario.is_admin = usuarioSchema.is_admin
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Usuario atualizado com sucesso",
                    "usuario": {
                        "id_usuario": usuario.id_usuario,
                        "email": usuario.email,
                        "is_admin": usuario.is_admin,
                    },
                },
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Usuario não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao atualizar usuario", "error": str(e)},
        )


@router.delete("/usuario", tags=["Usuario"])
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Usuario deletado com sucesso"},
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Usuario não encontrado"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao deletar usuario", "error": str(e)},
        )
