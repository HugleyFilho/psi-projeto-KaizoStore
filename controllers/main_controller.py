from flask import Blueprint, render_template, redirect, url_for, session, flash
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria, Jogo, Jogador

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
        favoritos = set()
        if "jogador_id" in session:
            jogador = db_session.get(Jogador, session["jogador_id"])
            if jogador:
                favoritos = {j.id for j in jogador.jogos_favoritos}
        return render_template("catalogo.html", jogos=jogos, categorias=categorias, favoritos=favoritos)





@main_bp.route("/favoritar/<int:jogo_id>", methods=["POST"])
def favoritar_jogo(jogo_id):
    if "jogador_id" not in session:
        flash("Faça login para favoritar jogos.")
        return redirect(url_for("auth.login"))

    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, session["jogador_id"])
        jogo = db_session.get(Jogo, jogo_id)

        if jogo and jogador:
            if jogo in jogador.jogos_favoritos:
                jogador.jogos_favoritos.remove(jogo)
                flash("Jogo removido dos favoritos.")
            else:
                jogador.jogos_favoritos.append(jogo)
                flash("Jogo adicionado aos favoritos!")
            db_session.commit()

    return redirect(url_for("main.catalogo"))
