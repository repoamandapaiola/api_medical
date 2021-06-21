from flask import Blueprint, request, current_app
from marshmallow import ValidationError

from controller.prescriptions import PrescriptionsController
from dao.mongo_dao import PrescriptionMongoDAO
from views.schemas.factory_schema_error import create_schema_error, ErrorCode
from views.schemas.prescriptions import PrescriptionsCreateSchema

prescriptions_blueprint = Blueprint('user', __name__, url_prefix='/prescriptions')


@prescriptions_blueprint.route('/', methods=['POST'])
def add():
    try:
        db = current_app.config['database']
        prescriptions = PrescriptionsCreateSchema().load(request.json)
        mongo_prescription_dao = PrescriptionMongoDAO(mongo_session=db)
        controller = PrescriptionsController(dao=mongo_prescription_dao, clinic_service=current_app.config['clinic_service'],
                                             metric_service=current_app.config['metric_service'],
                                             patient_service=current_app.config['patient_service'],
                                             physician_service=current_app.config['physician_service'])
        response, status_code = controller.create_prescription(clinic_id=prescriptions["clinic"]["id"],
                                                               physician_id=prescriptions["physician"]["id"],
                                                               patient_id=prescriptions["patient"]["id"],
                                                               text=prescriptions["text"])
        return response, status_code
    except ValidationError:
        schema_error = create_schema_error(ErrorCode.MALFORMED.value)
        return schema_error, 400
