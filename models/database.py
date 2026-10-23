from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite:///kaizostore.db"

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass

def criar_banco():
    Base.metadata.create_all(bind=engine)