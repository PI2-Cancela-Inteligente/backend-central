from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import carro, usuario, estaciona, motorista, cartao, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(carro.router, tags=["Carro"])
app.include_router(usuario.router, tags=["Usuario"])
app.include_router(estaciona.router, tags=["Estaciona"])
app.include_router(motorista.router, tags=["Motorista"])
app.include_router(cartao.router, tags=["Cartao"])
app.include_router(auth.router, tags=["Autenticacao"])


@app.get("/", tags=["Root"])
def root():
    return {"APP": "Backend is running"}
