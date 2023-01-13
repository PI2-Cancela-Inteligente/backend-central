import os

from dotenv import load_dotenv

load_dotenv("config/.env")


class Env:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_URL = os.getenv("DATABASE_URL")

    def __str__(self) -> str:
        return f"Envs({self.__dict__})"

    def __repr__(self) -> str:
        return f"Envs({self.__dict__})"

    def __dict__(self) -> dict:
        return {
            "MAIL_USERNAME": self.MAIL_USERNAME,
            "MAIL_PASSWORD": self.MAIL_PASSWORD,
            "MAIL_FROM": self.MAIL_FROM,
            "MAIL_PORT": self.MAIL_PORT,
            "MAIL_SERVER": self.MAIL_SERVER,
            "DB_HOST": self.DB_HOST,
            "DB_PORT": self.DB_PORT,
            "DB_NAME": self.DB_NAME,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
        }
