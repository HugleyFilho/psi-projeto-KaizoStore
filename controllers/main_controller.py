from flask import Blueprint, render_template
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria, Jogo

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    with Session(engine) as db_session:
        jogos = db_session.query(Jogo).limit(6).all()
        return render_template("index.html", jogos=jogos)


@main_bp.route("/catalogo")
def catalogo():
    with Session(engine) as db_session:
        jogos = db_session.query(Jogo).all()
        categorias = db_session.query(Categoria).all()
        return render_template("catalogo.html", jogos=jogos, categorias=categorias)


