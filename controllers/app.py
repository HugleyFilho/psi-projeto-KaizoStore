from flask import Flask
from models.database import Base, engine
from controllers.categoria_controller import categoria_bp


def criar_banco():
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)

app.register_blueprint(categoria_bp)

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)