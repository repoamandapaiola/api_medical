import load_config
from pymongo import MongoClient

from app.app import create_app
from services.clinics import ClinicService
from services.metrics import MetricsService
from services.patient import PatientService
from services.physicians import PhysiciansService

client = MongoClient(host='localhost')
out_service_url = 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'
app = create_app(session_database=client,
                 clinic_service=ClinicService(url=out_service_url),
                 patient_service=PatientService(url=out_service_url),
                 physician_service=PhysiciansService(url=out_service_url),
                 metric_service=MetricsService(url=out_service_url))

app.run('0.0.0.0', port=9090)