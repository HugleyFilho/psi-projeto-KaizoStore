from flask import Blueprint
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria, Jogo

main_bp = Blueprint("main", __name__)



@main_bp.route("/")
def index():
    with Session(engine) as db_session:
        jogos = db_session.query(Jogo).limit(6).all()
    return ""


@main_bp.route("/catalogo")
def catalogo():
    with Session(engine) as db_session:
        jogos = db_session.query(Jogo).all()
        categorias = db_session.query(Categoria).all()
    return ""

@main_bp.route("/sobre")
def sobre():
    return ""