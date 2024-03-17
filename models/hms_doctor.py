from odoo import fields, models, api


class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'first_name'


    first_name = fields.Char()
    last_name=fields.Char()
    image=fields.Image()
    patients_ids=fields.One2many('hms.patient.doctor','doctor_id')

