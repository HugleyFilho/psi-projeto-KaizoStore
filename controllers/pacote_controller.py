from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Jogo, PacoteItem

pacote_bp = Blueprint("pacote", __name__, url_prefix="/pacotes")


@pacote_bp.route("/")
def listar():
    with Session(engine) as db_session:
        pacotes = db_session.query(PacoteItem).all()
        return render_template("pacotes/lista.html", pacotes=pacotes)


@pacote_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as db_session:
        pacote = db_session.get(PacoteItem, id)
        if not pacote:
            flash("Pacote não encontrado.")
            return redirect(url_for("pacote.listar"))
        return render_template("pacotes/detalhe.html", pacote=pacote)


@pacote_bp.route("/criar", methods=["GET", "POST"])
def criar():
    with Session(engine) as db_session:
        if request.method == "POST":
            db_session.add(PacoteItem(
                nome=request.form.get("nome"),
                quantidade_moeda=request.form.get("quantidade_moeda", type=int) or 0,
                preco=request.form.get("preco", type=float) or 0.0,
                jogo_id=request.form.get("jogo_id", type=int),
            ))
            db_session.commit()
            flash("Pacote criado.")
            return redirect(url_for("pacote.listar"))

        jogos = db_session.query(Jogo).all()
        return render_template("pacotes/form.html", pacote=None, jogos=jogos)


@pacote_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with Session(engine) as db_session:
        pacote = db_session.get(PacoteItem, id)
        if not pacote:
            flash("Pacote não encontrado.")
            return redirect(url_for("pacote.listar"))

        if request.method == "POST":
            pacote.nome = request.form.get("nome")
            pacote.quantidade_moeda = request.form.get("quantidade_moeda", type=int) or 0
            pacote.preco = request.form.get("preco", type=float) or 0.0
            pacote.jogo_id = request.form.get("jogo_id", type=int)
            db_session.commit()
            flash("Pacote atualizado.")
            return redirect(url_for("pacote.listar"))

        jogos = db_session.query(Jogo).all()
        return render_template("pacotes/form.html", pacote=pacote, jogos=jogos)


@pacote_bp.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    with Session(engine) as db_session:
        pacote = db_session.get(PacoteItem, id)
        if not pacote:
            flash("Pacote não encontrado.")
        else:
            db_session.delete(pacote)
            db_session.commit()
            flash("Pacote excluído.")
    return redirect(url_for("pacote.listar"))
