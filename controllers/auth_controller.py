from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from models.database import engine
from models.models import Jogador

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        email = request.form.get("email")
        senha = request.form.get("senha")

        with Session(engine) as db_session:
            existe = db_session.query(Jogador).filter(
                (Jogador.nickname == nickname) | (Jogador.email == email)
            ).first()
            if existe:
                flash("Nickname ou e-mail já cadastrado.")
                return redirect(url_for("auth.cadastro"))

            novo_jogador = Jogador(
                nickname=nickname,
                email=email,
                senha_hash=generate_password_hash(senha),
            )
            db_session.add(novo_jogador)
            db_session.commit()

        flash("Conta criada! Faça login.")
        return redirect(url_for("auth.login"))
    return render_template("cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        with Session(engine) as db_session:
            jogador = db_session.query(Jogador).filter(Jogador.email == email).first()
            if jogador and check_password_hash(jogador.senha_hash, senha):
                session["jogador_id"] = jogador.id
                session["jogador_nickname"] = jogador.nickname
                return redirect(url_for("main.index"))

        flash("E-mail ou senha incorretos.")
        return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
