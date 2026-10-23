from flask import Blueprint, request
from sqlalchemy.orm import Session

from models.database import engine
from models.models import PacoteItem

pacote_bp = Blueprint("pacote", __name__, url_prefix="/pacotes")


@pacote_bp.route("/")
def listar():
    with Session(engine) as db_session:
        pacotes = db_session.query(PacoteItem).all()
    return ""

@pacote_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as db_session:
        pacote = db_session.query(PacoteItem).filter(PacoteItem.id == id).first()
    return ""

@pacote_bp.route("/criar")
def criar():
    nome = request.args.get("nome")
    quantidade_moeda = request.args.get("quantidade_moeda", type=int)
    preco = request.args.get("preco", type=float)
    jogo_id = request.args.get("jogo_id", type=int)

    if nome and jogo_id:
        with Session(engine) as db_session:
            novo_pacote = PacoteItem(
                nome=nome,
                quantidade_moeda=quantidade_moeda or 0,
                preco=preco or 0.0,
                jogo_id=jogo_id,
            )
            db_session.add(novo_pacote)
            db_session.commit()
    return ""

@pacote_bp.route("/editar/<int:id>")
def editar(id):
    nome = request.args.get("nome")
    quantidade_moeda = request.args.get("quantidade_moeda", type=int)
    preco = request.args.get("preco", type=float)
    jogo_id = request.args.get("jogo_id", type=int)

    with Session(engine) as db_session:
        pacote = db_session.query(PacoteItem).filter(PacoteItem.id == id).first()
        if pacote:
            if nome:
                pacote.nome = nome
            if quantidade_moeda is not None:
                pacote.quantidade_moeda = quantidade_moeda
            if preco is not None:
                pacote.preco = preco
            if jogo_id:
                pacote.jogo_id = jogo_id
            db_session.commit()
    return ""

@pacote_bp.route("/deletar/<int:id>")
def deletar(id):
    with Session(engine) as db_session:
        pacote = db_session.query(PacoteItem).filter(PacoteItem.id == id).first()
        if pacote:
            db_session.delete(pacote)
            db_session.commit()
    return ""