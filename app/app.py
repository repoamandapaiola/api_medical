from flask import Blueprint, Flask

from views.prescriptions import prescriptions_blueprint

home = Blueprint('home', import_name='home')


@home.route('/', methods=['POST'])
def home():
    return "Bem vindo. Estou rodando!"


def create_app(session_database):
    app = Flask(__name__)
    app.register_blueprint(prescriptions_blueprint)
    app.config['database'] = session_database

    return app
