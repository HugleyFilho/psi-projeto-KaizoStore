from flask import Blueprint, request
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Categoria

categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")

@categoria_bp.route("/")
def listar():
    with Session(engine) as session:
        categorias = session.query(Categoria).all()
    return ""

@categoria_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as session:
        categoria = session.query(Categoria).filter(Categoria.id == id).first()
    return ""

@categoria_bp.route("/criar")
def criar():
    nome = request.args.get("nome")
    descricao = request.args.get("descricao")

    if nome:
        with Session(engine) as session:
            nova_categoria = Categoria(nome=nome, descricao=descricao)
            session.add(nova_categoria)
            session.commit()
    return ""

@categoria_bp.route("/editar/<int:id>")
def editar(id):
    nome = request.args.get("nome")
    descricao = request.args.get("descricao")

    with Session(engine) as session:
        categoria = session.query(Categoria).filter(Categoria.id == id).first()
        if categoria:
            if nome:
                categoria.nome = nome
            if descricao:
                categoria.descricao = descricao
            session.commit()
    return ""

@categoria_bp.route("/deletar/<int:id>")
def deletar(id):
    with Session(engine) as session:
        categoria = session.query(Categoria).filter(Categoria.id == id).first()
        if categoria:
            session.delete(categoria)
            session.commit()
    return ""