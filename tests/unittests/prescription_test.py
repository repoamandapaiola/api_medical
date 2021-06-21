import unittest
import json

from app.app import create_app
from pymongo import MongoClient


class SignupTest(unittest.TestCase):

    def setUp(self):
        client = MongoClient(host='localhost')
        app = create_app(client)
        self.app = app.test_client()

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
        pass
