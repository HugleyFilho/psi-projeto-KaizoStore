from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session

from models.database import engine
from models.models import Jogador, Jogo, PacoteItem

jogador_bp = Blueprint("jogador", __name__, url_prefix="/jogadores")


def _voltar(jogador_id):
    return redirect(request.referrer or url_for("jogador.buscar", id=jogador_id))


@jogador_bp.route("/")
def listar():
    with Session(engine) as db_session:
        jogadores = db_session.query(Jogador).all()
        return render_template("jogadores/lista.html", jogadores=jogadores)


@jogador_bp.route("/<int:id>")
def buscar(id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        if not jogador:
            flash("Jogador não encontrado.")
            return redirect(url_for("jogador.listar"))
        jogos = db_session.query(Jogo).all()
        pacotes = db_session.query(PacoteItem).all()
        return render_template("jogadores/detalhe.html", jogador=jogador, jogos=jogos, pacotes=pacotes)


@jogador_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        if not jogador:
            flash("Jogador não encontrado.")
            return redirect(url_for("jogador.listar"))

        if request.method == "POST":
            nickname = request.form.get("nickname")
            email = request.form.get("email")
            repetido = db_session.query(Jogador).filter(
                (Jogador.nickname == nickname) | (Jogador.email == email),
                Jogador.id != id,
            ).first()
            if repetido:
                flash("Nickname ou e-mail já cadastrado.")
                return redirect(url_for("jogador.editar", id=id))

            jogador.nickname = nickname
            jogador.email = email
            db_session.commit()
            flash("Jogador atualizado.")
            return redirect(url_for("jogador.buscar", id=id))
        return render_template("jogadores/form.html", jogador=jogador)


@jogador_bp.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        if not jogador:
            flash("Jogador não encontrado.")
        else:
            # as linhas das tabelas N:N (jogador_jogo / jogador_pacote) saem junto
            db_session.delete(jogador)
            db_session.commit()
            flash("Jogador excluído.")
    return redirect(url_for("jogador.listar"))


# ---------- N:N Jogador <-> Jogo (favoritos) ----------

@jogador_bp.route("/<int:id>/jogos", methods=["POST"])
def vincular_jogo(id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        jogo = db_session.get(Jogo, request.form.get("jogo_id", type=int))
        if not jogador or not jogo:
            flash("Jogador ou jogo não encontrado.")
        elif jogo in jogador.jogos_favoritos:
            flash("Este jogo já está nos favoritos.")
        else:
            jogador.jogos_favoritos.append(jogo)
            db_session.commit()
            flash("Jogo adicionado aos favoritos!")
    return _voltar(id)


@jogador_bp.route("/<int:id>/jogos/<int:jogo_id>/remover", methods=["POST"])
def desvincular_jogo(id, jogo_id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        jogo = db_session.get(Jogo, jogo_id)
        if jogador and jogo and jogo in jogador.jogos_favoritos:
            jogador.jogos_favoritos.remove(jogo)
            db_session.commit()
            flash("Jogo removido dos favoritos.")
        else:
            flash("Vínculo não encontrado.")
    return _voltar(id)


# ---------- N:N Jogador <-> PacoteItem (adquiridos) ----------

@jogador_bp.route("/<int:id>/pacotes", methods=["POST"])
def vincular_pacote(id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        pacote = db_session.get(PacoteItem, request.form.get("pacote_id", type=int))
        if not jogador or not pacote:
            flash("Jogador ou pacote não encontrado.")
        elif pacote in jogador.pacotes_adquiridos:
            flash("Você já possui este pacote.")
        else:
            jogador.pacotes_adquiridos.append(pacote)
            db_session.commit()
            flash("Pacote adquirido com sucesso!")
    return _voltar(id)


@jogador_bp.route("/<int:id>/pacotes/<int:pacote_id>/remover", methods=["POST"])
def desvincular_pacote(id, pacote_id):
    with Session(engine) as db_session:
        jogador = db_session.get(Jogador, id)
        pacote = db_session.get(PacoteItem, pacote_id)
        if jogador and pacote and pacote in jogador.pacotes_adquiridos:
            jogador.pacotes_adquiridos.remove(pacote)
            db_session.commit()
            flash("Pacote removido.")
        else:
            flash("Vínculo não encontrado.")
    return _voltar(id)
