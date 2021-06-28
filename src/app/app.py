from flask import Blueprint, Flask

from src.services.service_abc import ServiceABC
from src.views.prescriptions import prescriptions_blueprint

home = Blueprint('home', import_name='home')


@home.route('/', methods=['POST'])
def home():
    return "Bem vindo. Estou rodando!"


def create_app(session_database, clinic_service: ServiceABC, patient_service: ServiceABC,
               physician_service: ServiceABC, metric_service: ServiceABC):
    app = Flask(__name__)
    app.register_blueprint(prescriptions_blueprint)
    app.config['database'] = session_database
    app.config['clinic_service'] = clinic_service
    app.config['patient_service'] = patient_service
    app.config['physician_service'] = physician_service
    app.config['metric_service'] = metric_service

    return app
