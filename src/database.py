from src.env import Env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = Env()

DATABASE_URL = env.DATABASE_URL
if not DATABASE_URL.startswith("sqlite"):
    DATABASE_URL += "/backend-estacionamento"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()