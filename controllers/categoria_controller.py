from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria

categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")


@categoria_bp.route("/")
def listar():
    with Session(engine) as db_session:
        categorias = db_session.query(Categoria).all()
        return render_template("categorias/lista.html", categorias=categorias)


@categoria_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as db_session:
        categoria = db_session.get(Categoria, id)
        if not categoria:
            flash("Categoria não encontrada.")
            return redirect(url_for("categoria.listar"))
        return render_template("categorias/detalhe.html", categoria=categoria)


@categoria_bp.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.form.get("nome")
        with Session(engine) as db_session:
            if db_session.query(Categoria).filter(Categoria.nome == nome).first():
                flash("Já existe uma categoria com esse nome.")
                return redirect(url_for("categoria.criar"))

            db_session.add(Categoria(nome=nome, descricao=request.form.get("descricao")))
            db_session.commit()
        flash("Categoria criada.")
        return redirect(url_for("categoria.listar"))
    return render_template("categorias/form.html", categoria=None)


@categoria_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with Session(engine) as db_session:
        categoria = db_session.get(Categoria, id)
        if not categoria:
            flash("Categoria não encontrada.")
            return redirect(url_for("categoria.listar"))

        if request.method == "POST":
            nome = request.form.get("nome")
            repetida = db_session.query(Categoria).filter(
                Categoria.nome == nome, Categoria.id != id
            ).first()
            if repetida:
                flash("Já existe uma categoria com esse nome.")
                return redirect(url_for("categoria.editar", id=id))

            categoria.nome = nome
            categoria.descricao = request.form.get("descricao")
            db_session.commit()
            flash("Categoria atualizada.")
            return redirect(url_for("categoria.listar"))
        return render_template("categorias/form.html", categoria=categoria)


@categoria_bp.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    with Session(engine) as db_session:
        categoria = db_session.get(Categoria, id)
        if not categoria:
            flash("Categoria não encontrada.")
        elif categoria.jogos:
            flash("Não é possível excluir: a categoria ainda tem jogos.")
        else:
            db_session.delete(categoria)
            db_session.commit()
            flash("Categoria excluída.")
    return redirect(url_for("categoria.listar"))
