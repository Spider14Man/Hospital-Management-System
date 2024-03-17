from odoo import fields, models, api


class HmsCrm(models.Model):
    _inherit = 'crm.lead'
    related_patient_id = fields.Many2one('hms.patient')
