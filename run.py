import os

import load_config
from pymongo import MongoClient

from src.app.app import create_app
from src.services.clinics import ClinicService
from src.services.metrics import MetricsService
from src.services.patient import PatientService
from src.services.physicians import PhysiciansService

client = MongoClient(host=os.environ['MONGO_HOSTNAME'])
out_service_url = 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'
app = create_app(session_database=client,
                 clinic_service=ClinicService(url=out_service_url),
                 patient_service=PatientService(url=out_service_url),
                 physician_service=PhysiciansService(url=out_service_url),
                 metric_service=MetricsService(url=out_service_url))

app.run('0.0.0.0', port=5000)