import random

from odoo import fields, models, api
from odoo.exceptions import ValidationError,UserError

class HmsPatient(models.Model):
    _name = 'hms.patient'

    name = fields.Char(string="First Name", required=True)
    second_name=fields.Char()
    email=fields.Char(readonly="1")
    birth_date=fields.Date()
    history=fields.Html()
    cr_ratio=fields.Float()
    blood_type=fields.Selection([
        ('a','A'),
        ('o','O'),
        ('o2','O2')
    ])
    pcr=fields.Boolean()
    image=fields.Image()
    address=fields.Text()
    age=fields.Integer(compute="cal_age" )
    department_id=fields.Many2one('hms.department')
    doctors_ids=fields.One2many('hms.patient.doctor','patient_id')
    capcity_department=fields.Integer(related='department_id.capcity')
    states=fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious'),
    ],default="undetermined")
    log_history_ids=fields.One2many('log.history','patient_id')
    def patient_undetermined(self):
        self.states='undetermined'

    def patient_good(self):
        self.states='good'

    def patient_fair(self):
        self.states='fair'

    def patient_serious(self):
        self.states='serious'
    @api.onchange('pcr')
    def check_age(self):
        if self.age<30:
            return {
                'warning': {
            'title': "Warning",
            'message': "the bcr has been cheacked and the age is less than 30"
            }            }
    @api.depends('birth_date')
    def cal_age(self):
        for patient in self:
            if patient.birth_date:
                today=fields.Date.today()
                delta=(today-patient.birth_date).days
                patient.age=delta//365
            else:
                patient.age=0


    @api.model
    def create(self, vals):
        email=f'{vals.get("name")}.{vals.get("second_name")[0]}{random.randrange(100,999)}@Hms.com'
        vals['email']=email
        patient=super().create(vals)

        return patient

    def write(self, vals):
        if vals.get('name') or vals.get('second_name'):
            if vals.get('name'):
                email = f'{vals.get("name")}'
            else:
                email = f'{self.name}'
            if vals.get('second_name'):
                email += f'.{vals.get("second_name")[0]}{random.randrange(100,999)}@Hms.com'
            else:
                email+=f'.{self.second_name[0]}{random.randrange(100,999)}@Hms.com'
            vals['email']=email
        patient=super().write(vals)

        return patient

    def unlink(self):
        for patient in self:
            if patient.department_id:
                raise UserError(f'can\'t delete {patient.name} becuase he releated with department')
        return super().unlink()
    _sql_constraints = [
        ('email_unique','unique("email")','there was existence email and no be valid')
    ]
class HmsLogHistory(models.Model):
    _name = 'log.history'


    description=fields.Html()
    patient_id=fields.Many2one('hms.patient')