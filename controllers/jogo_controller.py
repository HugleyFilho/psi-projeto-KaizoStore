from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria, Jogo

jogo_bp = Blueprint("jogo", __name__, url_prefix="/jogos")


@jogo_bp.route("/")
def listar():
    with Session(engine) as db_session:
        jogos = db_session.query(Jogo).all()
        return render_template("jogos/lista.html", jogos=jogos)


@jogo_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as db_session:
        jogo = db_session.get(Jogo, id)
        if not jogo:
            flash("Jogo não encontrado.")
            return redirect(url_for("jogo.listar"))
        return render_template("jogos/detalhe.html", jogo=jogo)


@jogo_bp.route("/criar", methods=["GET", "POST"])
def criar():
    with Session(engine) as db_session:
        if request.method == "POST":
            categoria_id = request.form.get("categoria_id", type=int)
            if not db_session.get(Categoria, categoria_id):
                flash("Escolha uma categoria válida.")
                return redirect(url_for("jogo.criar"))

            db_session.add(Jogo(
                titulo=request.form.get("titulo"),
                descricao=request.form.get("descricao"),
                preco=request.form.get("preco", type=float) or 0.0,
                categoria_id=categoria_id,  # 1:N - Categoria possui vários Jogos
            ))
            db_session.commit()
            flash("Jogo criado.")
            return redirect(url_for("jogo.listar"))

        categorias = db_session.query(Categoria).all()
        if not categorias:
            flash("Cadastre uma categoria antes de criar um jogo.")
            return redirect(url_for("categoria.criar"))
        return render_template("jogos/form.html", jogo=None, categorias=categorias)


@jogo_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with Session(engine) as db_session:
        jogo = db_session.get(Jogo, id)
        if not jogo:
            flash("Jogo não encontrado.")
            return redirect(url_for("jogo.listar"))

        if request.method == "POST":
            categoria_id = request.form.get("categoria_id", type=int)
            if not db_session.get(Categoria, categoria_id):
                flash("Escolha uma categoria válida.")
                return redirect(url_for("jogo.editar", id=id))

            jogo.titulo = request.form.get("titulo")
            jogo.descricao = request.form.get("descricao")
            jogo.preco = request.form.get("preco", type=float) or 0.0
            jogo.categoria_id = categoria_id
            db_session.commit()
            flash("Jogo atualizado.")
            return redirect(url_for("jogo.listar"))

        categorias = db_session.query(Categoria).all()
        return render_template("jogos/form.html", jogo=jogo, categorias=categorias)


@jogo_bp.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    with Session(engine) as db_session:
        jogo = db_session.get(Jogo, id)
        if not jogo:
            flash("Jogo não encontrado.")
        elif jogo.pacotes_itens:
            flash("Não é possível excluir: o jogo ainda tem pacotes de itens.")
        else:
            # os favoritos (N:N) são removidos automaticamente da tabela jogador_jogo
            db_session.delete(jogo)
            db_session.commit()
            flash("Jogo excluído.")
    return redirect(url_for("jogo.listar"))
