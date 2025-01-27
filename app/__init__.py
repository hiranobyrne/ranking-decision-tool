from flask import Flask
from flask_session import Session
from app.routes import main
from config import Config
# import os
from app.routes.dash_routes import create_dash_app


def create_app():
    app = Flask(__name__)

    # codigo do './frontend'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False


    # carregar todas configurações da classe Config em config.py
    # eh necessario para usar sessoes, que sao usadas na tela de preencher os pesos (ahp_3_matrices.html)
    app.config.from_object(Config)

    # app.config['DATA_FILE'] = './data/ahp_cars.csv' # funciona localmente, mas nao funciona em deploy em outra maquina
    # app.config['DATA_FILE'] = os.path.join(os.path.dirname(__file__), '../data/ahp_cars.csv') # usado no deploy do render

    # nao precisa, esta configuracao jah estah em config.py
    # app.config['DATA_DIR'] = os.path.join(os.path.dirname(__file__), '../data')

    # registro das blueprints
    app.register_blueprint(main)

    create_dash_app(app)

    Session(app) # codigo do './frontend'

    # Load configuration dynamically based on the app's root path
    # config = Config(app.root_path) # codigo do './frontend'

    return app
