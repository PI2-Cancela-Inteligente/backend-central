from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

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
def get_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()
        if usuarios:
            return [usuario.to_dict() for usuario in usuarios]
        return {"message": "Nenhum usuario encontrado"}
    except Exception as e:
        return {"message": "Erro ao buscar usuarios", "error": str(e)}


@router.post("/usuario", tags=["Usuario"])
def create_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    try:
        usuario = Usuario(**usuario.dict())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario.to_dict()
    except Exception as e:
        return {"message": "Erro ao criar usuario", "error": str(e)}


@router.put("/usuario", tags=["Usuario"])
def update_usuario(
    id_usuario: int,
    usuarioSchema: UsuarioSchema,
    db: Session = Depends(get_db),
):
    try:
        usuario = (
            db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if usuario:
            usuario.email = usuarioSchema.email
            if usuarioSchema.senha:
                usuario.senha = usuarioSchema.senha
            usuario.is_admin = usuarioSchema.is_admin
            db.commit()
            return usuario.to_dict()
        return {"message": "Usuario não encontrado"}
    except Exception as e:
        return {"message": "Erro ao atualizar usuario", "error": str(e)}


@router.delete("/usuario", tags=["Usuario"])
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        usuario = (
            db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if usuario:
            db.delete(usuario)
            db.commit()
            return {"message": "Usuario deletado com sucesso"}
        return {"message": "Usuario não encontrado"}
    except Exception as e:
        return {"message": "Erro ao deletar usuario", "error": str(e)}
