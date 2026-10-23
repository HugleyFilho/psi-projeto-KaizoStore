from flask import Blueprint, request, session
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from models.database import engine
from models.models import Jogador

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/cadastro")
def cadastro():
    nickname = request.args.get("nickname")
    email = request.args.get("email")
    senha = request.args.get("senha")

    if nickname and email and senha:
        senha_hash = generate_password_hash(senha)
        with Session(engine) as db_session:
            novo_jogador = Jogador(
                nickname=nickname, email=email, senha_hash=senha_hash
            )
            db_session.add(novo_jogador)
            db_session.commit()
    return ""

@auth_bp.route("/login")
def login():
    email = request.args.get("email")
    senha = request.args.get("senha")

    if email and senha:
        with Session(engine) as db_session:
            jogador = (
                db_session.query(Jogador)
                .filter(Jogador.email == email)
                .first()
            )
            if jogador and check_password_hash(jogador.senha_hash, senha):
                session["jogador_id"] = jogador.id
                session["jogador_nickname"] = jogador.nickname
    return ""

@auth_bp.route("/logout")
def logout():
    session.clear()
    return ""