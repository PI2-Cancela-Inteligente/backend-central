from fastapi import FastAPI

from src.routers import carro, usuario, estaciona

app = FastAPI()


app.include_router(carro.router, tags=["Carro"])
app.include_router(usuario.router, tags=["Usuario"])
app.include_router(estaciona.router, tags=["Estaciona"])


@app.get("/", tags=["Root"])
def root():
    return {"APP": "Backend is running"}
