from flask import Flask
from models.database import Base, engine

from controllers.auth_controller import auth_bp
from controllers.categoria_controller import categoria_bp
from controllers.main_controller import main_bp
from controllers.pacote_controller import pacote_bp

def criar_banco():
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = "kaizostore"

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(pacote_bp)

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)