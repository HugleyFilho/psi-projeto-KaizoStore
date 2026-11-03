from flask import Flask, redirect, request, session, url_for

from models.database import Base, engine
import models.models

from controllers.auth_controller import auth_bp
from controllers.categoria_controller import categoria_bp
from controllers.jogador_controller import jogador_bp
from controllers.jogo_controller import jogo_bp
from controllers.main_controller import main_bp
from controllers.pacote_controller import pacote_bp


def criar_banco():
    Base.metadata.create_all(bind=engine)


app = Flask(__name__)
app.secret_key = "kaizostore"

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(jogo_bp)
app.register_blueprint(pacote_bp)
app.register_blueprint(jogador_bp)

publica = {"auth.cadastro", "auth.login", "static"}


@app.before_request
def exigir_login():
    if request.endpoint in publica:
        if session.get("jogador_id") and request.endpoint != "static":
            return redirect(url_for("main.index"))
        return None
    if not session.get("jogador_id"):
        return redirect(url_for("auth.cadastro"))


criar_banco()

if __name__ == "__main__":
    app.run(debug=True)