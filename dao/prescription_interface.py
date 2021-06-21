from abc import ABC


class PrescriptioDAOI(ABC):

    def add(self, clinic_id, physician_id, patient_id, text):
        pass

    def remove(self, id: str):
        pass
