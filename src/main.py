from fastapi import FastAPI

from src.routers import carro

app = FastAPI()


app.include_router(carro.router, tags=["Carro"])


@app.get("/", tags=["Root"])
def root():
    return {"APP": "Backend is running"}

