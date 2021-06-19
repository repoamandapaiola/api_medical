from flask import Blueprint, request

from views.schemas.prescriptions import PrescriptionsCreateSchema

prescriptions_blueprint = Blueprint('user', __name__, url_prefix='/prescriptions')


@prescriptions_blueprint.route('/', methods=['GET'])
def show():
    #TODO show prescriptions_blueprint
    return ["Amanda", "Pedro", "Will"]


@prescriptions_blueprint.route('/', methods=['POST'])
def add():
    loaded = PrescriptionsCreateSchema().validate(request.json)
    if len(loaded) > 0:
        return f'Erro: {loaded}', 400
    #TODO chamar a inserção
    return "Inserido"

