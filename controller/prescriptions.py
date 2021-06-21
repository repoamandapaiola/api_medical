from dao.prescription_interface import PrescriptioDAOI

from exceptions.api_exceptions import NotFound, ServiceNotAvailable
from services.clinics import ClinicDTO, ClinicService
from services.metrics import MetricsService, MetricsDTO
from services.patient import PatientService
from services.physicians import PhysiciansService
from views.schemas.factory_schema_error import create_schema_error, ErrorCode
from views.schemas.prescriptions import create_response_schema


class PrescriptionsController:
    def __init__(self, dao: PrescriptioDAOI):
        self.dao = dao
        self.clinic_service = ClinicService()
        self.metrics_service = MetricsService()
        self.patient_service = PatientService()
        self.physician_service = PhysiciansService()

    def create_prescription(self, clinic_id: int, physician_id: int, patient_id: int,
                            text: str):
        try:
            clinic_dto = self.clinic_service.get(clinic_id)
        except (NotFound, ServiceNotAvailable):
            clinic_dto = ClinicDTO(id_=clinic_id, name='')

        try:
            patient_dto = self.patient_service.get(patient_id)
        except (NotFound, ServiceNotAvailable) as e:
            if isinstance(e, NotFound):
                return create_schema_error(error_code=ErrorCode.PATIENT_NOT_FOUND.value), 400
            else:
                return create_schema_error(error_code=ErrorCode.PATIENT_NOT_AVAILABLE.value), 400

        try:
            physician_dto = self.physician_service.get(physician_id=physician_id)
        except (NotFound, ServiceNotAvailable) as e:
            if isinstance(e, NotFound):
                return create_schema_error(error_code=ErrorCode.PHYSICIAN_NOT_FOUND.value), 400
            else:
                return create_schema_error(error_code=ErrorCode.PHYSICIAN_NOT_AVAILABLE.value), 400

        p_id = self.dao.add(clinic_id=clinic_id, physician_id=physician_id,
                            patient_id=patient_id, text=text)

        metric = MetricsDTO(clinic_id=clinic_id, clinic_name=clinic_dto.name,
                            physician_id=physician_dto.id,
                            physician_name=physician_dto.name,
                            physician_crm=physician_dto.crm,
                            patient_id=patient_dto.id,
                            patient_name=patient_dto.name,
                            patient_email=patient_dto.email,
                            patient_phone=patient_dto.phone)
        self.metrics_service.post(metric=metric)

        return create_response_schema(p_id=p_id, clinic_id=clinic_id,
                                      physician_id=physician_id, patient_id=patient_id,
                                      text=text), 200
