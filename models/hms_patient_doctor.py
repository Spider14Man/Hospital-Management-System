from odoo import fields, models, api


class Hms_doctor_patient_rel(models.Model):
    _name = 'hms.patient.doctor'

    name=fields.Char()
    patient_id=fields.Many2one('hms.patient')
    doctor_id=fields.Many2one('hms.doctor')
