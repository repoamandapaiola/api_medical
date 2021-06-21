import os

from dao.prescription_interface import PrescriptioDAOI


class PrescriptionMongoDAO(PrescriptioDAOI):
    def __init__(self, mongo_session):
        table = mongo_session.get_database(os.environ['MONGO_DATABASE']).get_collection(os.environ['MONGO_COLLECTION'])
        self.mongo_session=table

    def add(self, clinic_id: int, physician_id: int, patient_id: int,
            text: str):
        self.mongo_session.insert(
                    {
          "clinic": {
            "id": clinic_id
          },
          "physician": {
            "id": physician_id
          },
          "patient": {
            "id": patient_id
          },
          "text": text
        }
        )