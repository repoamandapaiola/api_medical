from marshmallow import Schema, fields


class Clinic(Schema):
    clinic_id = fields.Integer(required=False, load_from="id", attribute="id")


class Physician(Schema):
    physician_id = fields.Integer(required=False, load_from="id", attribute="id")


class Patient(Schema):
    patient_id = fields.Integer(required=False, load_from="id", attribute="id")


class PrescriptionsCreateSchema(Schema):
    clinic = fields.Nested(Clinic, required=True)
    physician = fields.Nested(Physician, required=True)
    patient = fields.Nested(Patient, required=True)
    text = fields.String(required=True)

