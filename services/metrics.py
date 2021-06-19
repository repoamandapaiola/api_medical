import requests
from services.service_abc import ServiceABC


class MetricsDTO:
    def __init__(self, clinic_id, clinic_name, physician_id, physician_name, physician_crm, patient_id,
                 patient_name, patient_email, patient_phone, metric_id=None):
        self.patient_phone = patient_phone
        self.patient_email = patient_email
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.physician_crm = physician_crm
        self.physician_name = physician_name
        self.physician_id = physician_id
        self.clinic_name = clinic_name
        self.clinic_id = clinic_id
        self.metric_id = metric_id

    def to_json(self):
        to_json = {
            "clinic_id": self.clinic_id,
            "clinic_name": self.clinic_name,
            "physician_id": self.physician_id,
            "physician_name": self.physician_name,
            "physician_crm": self.physician_crm,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_email": self.patient_email,
            "patient_phone": self.patient_phone
        }
        if self.metric_id:
            to_json["id"] = self.metric_id
        return to_json


class MetricsService(ServiceABC):
    def __init__(self):
        self.authorization = 'Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': self.authorization}

    @property
    def url(self):
        return 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'

    @property
    def cache_ttl(self):
        return 0

    @property
    def timeout(self):
        return 6

    @property
    def retry(self):
        return 5

    @property
    def path(self):
        return '/metrics'

    def post(self, metric: MetricsDTO):
        url = self.url + self.path
        content = requests.post(url, json=metric.to_json(), headers=self.headers, timeout=self.timeout)
        json_content = self.validate_response(content)
        return MetricsDTO(json_content)
