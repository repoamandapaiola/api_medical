import os
import unittest
import json

from app.app import create_app
from pymongo import MongoClient

from services.clinics import ClinicService
from services.metrics import MetricsService
from services.patient import PatientService
from services.physicians import PhysiciansService


class AppTest(unittest.TestCase):

    def setup_mongo(self):
        import load_config  # LOAD das variaveis de ambiente
        self.client = MongoClient(host='localhost')
        self.table = self.client.get_database(
            os.environ['MONGO_DATABASE']).get_collection(os.environ['MONGO_COLLECTION'])
        self.table.delete_many({})  # limpando dados para iniciar testes

    def setUp(self):
        self.setup_mongo()
        out_service_url = 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'
        self.clinic_service = ClinicService(url=out_service_url)
        self.patient_service = PatientService(url=out_service_url)
        self.physician_service = PhysiciansService(url=out_service_url)
        self.metric_service = MetricsService(url=out_service_url)

        app = create_app(self.client,
                         clinic_service=self.clinic_service,
                         patient_service=self.patient_service,
                         physician_service=self.physician_service,
                         metric_service=self.metric_service)
        self.app = app.test_client()

    def tearDown(self):
        self.table.delete_many({})

    def test_invalid_schema__expected_400_status_code(self):
        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "oi": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = self.app.post('/prescriptions/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, content['error']['code'])
        self.assertEqual('malformed request', content['error']['message'])

    def test_service_patient_not_available__expected_400_status_code(self):
        app_patient_out = create_app(self.client,
                                     clinic_service=self.clinic_service,
                                     patient_service=PatientService(url='https://whatever.mockapi.io/v1'),
                                     physician_service=self.physician_service,
                                     metric_service=self.metric_service)
        self.app_patient_out = app_patient_out.test_client()

        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "id": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = self.app_patient_out.post('/prescriptions/', headers={"Content-Type": "application/json"},
                                             data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual(6, content['error']['code'])
        self.assertEqual('patients service not available', content['error']['message'])

    def test_service_physicians_not_available__expected_400_status_code(self):
        app_patient_out = create_app(self.client,
                                     clinic_service=self.clinic_service,
                                     patient_service=self.patient_service,
                                     physician_service=PhysiciansService(url='https://whatever.mockapi.io/v1'),
                                     metric_service=self.metric_service)
        self.app_patient_out = app_patient_out.test_client()

        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "id": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = self.app_patient_out.post('/prescriptions/', headers={"Content-Type": "application/json"},
                                             data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual(5, content['error']['code'])
        self.assertEqual('physicians service not available', content['error']['message'])

    def test_create__expected_create_prescription_200(self):
        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "id": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = self.app.post('/prescriptions/', headers={"Content-Type": "application/json"},
                                 data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertIsNotNone(content['data']['id'])
        self.assertEqual(content['data']['text'], 'Dipirona 1x ao dia')
        self.assertEqual(content['data']['clinic']['id'], 1)
        self.assertEqual(content['data']['physician']['id'], 1)
        self.assertEqual(content['data']['patient']['id'], 1)
        self.assertEqual(200, response.status_code)

        doc = self.table.find_one()
        self.assertEqual(doc['clinic']['id'], 1)
        self.assertEqual(doc['physician']['id'], 1)
        self.assertEqual(doc['patient']['id'], 1)
        self.assertEqual(doc['text'], 'Dipirona 1x ao dia')

    def test_create_prescription__clinic_service_not_available(self):
        app_clinic_out = create_app(self.client,
                                    clinic_service=ClinicService(url='https://whatever.mockapi.io/v1'),
                                    patient_service=self.patient_service,
                                    physician_service=self.physician_service,
                                    metric_service=self.metric_service)
        app = app_clinic_out.test_client()
        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "id": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = app.post('/prescriptions/', headers={"Content-Type": "application/json"},
                            data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertIsNotNone(content['data']['id'])
        self.assertEqual(content['data']['text'], 'Dipirona 1x ao dia')
        self.assertEqual(content['data']['clinic']['id'], 1)
        self.assertEqual(content['data']['physician']['id'], 1)
        self.assertEqual(content['data']['patient']['id'], 1)
        self.assertEqual(200, response.status_code)

        doc = self.table.find_one()
        self.assertEqual(doc['clinic']['id'], 1)
        self.assertEqual(doc['physician']['id'], 1)
        self.assertEqual(doc['patient']['id'], 1)
        self.assertEqual(doc['text'], 'Dipirona 1x ao dia')

    def test_metrics_not_available__expected_500_not_save_prescription(self):
        app_clinic_out = create_app(self.client,
                                    clinic_service=self.clinic_service,
                                    patient_service=self.patient_service,
                                    physician_service=self.physician_service,
                                    metric_service=MetricsService(url='https://whatever.mockapi.io/v1'))
        app = app_clinic_out.test_client()
        # Given
        payload = json.dumps({
            "clinic": {
                "id": 1
            },
            "physician": {
                "id": 1
            },
            "patient": {
                "id": 1
            },
            "text": "Dipirona 1x ao dia"
        })

        # When
        response = app.post('/prescriptions/', headers={"Content-Type": "application/json"},
                            data=payload)

        # Then
        content = json.loads(response.data.decode())
        self.assertEqual(500, response.status_code)
        self.assertEqual(5, content['error']['code'])
        self.assertEqual('metrics service not available', content['error']['message'])

        doc = self.table.find_one()
        self.assertIsNone(doc)
