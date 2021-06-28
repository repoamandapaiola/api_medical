from marshmallow import Schema, fields


class Clinic(Schema):
    clinic_id = fields.Integer(required=False, data_key="id", attribute="id")


class Physician(Schema):
    physician_id = fields.Integer(required=False, data_key="id", attribute="id")


class Patient(Schema):
    patient_id = fields.Integer(required=False, data_key="id", attribute="id")


class PrescriptionsCreateSchema(Schema):
    clinic = fields.Nested(Clinic, required=True)
    physician = fields.Nested(Physician, required=True)
    patient = fields.Nested(Patient, required=True)
    text = fields.String(required=True)


def create_response_schema(p_id, clinic_id, physician_id, patient_id, text):
    return {
          "data": {
            "id": p_id,
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
        }
