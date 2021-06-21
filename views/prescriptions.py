from flask import Blueprint, request, current_app
from marshmallow import ValidationError

from controller.prescriptions import PrescriptionsController
from views.schemas.factory_schema_error import create_schema_error, ErrorCode
from views.schemas.prescriptions import PrescriptionsCreateSchema

prescriptions_blueprint = Blueprint('user', __name__, url_prefix='/prescriptions')


@prescriptions_blueprint.route('/', methods=['POST'])
def add():
    try:
        db = current_app.config['database']
        p_schema = PrescriptionsCreateSchema().load(request.json)
        controller = PrescriptionsController(db)
        response, status_code = controller.create_prescription(clinic_id=p_schema.clinic.clinic_id,
                                                               physician_id=p_schema.physician.physician_id,
                                                               patient_id=p_schema.patient.patient_id,
                                                               text=p_schema.text)
        return response, status_code
    except ValidationError:
        schema_error = create_schema_error(ErrorCode.MALFORMED.value)
        return schema_error, 400
