from odoo import models,fields


class CollegeTeacher(models.Model):
    _name = 'college.teacher'
    name = fields.Char('Name Teacher :',required=True )
    contract_date = fields.Date('Contrac Date')
    time_working= fields.Integer('Time Working')
    defined_contract = fields.Boolean('Defined Contract',groups='universidad_admin.group_college_principal')
    last_modification = fields.Date('last Modification',readonly = True)
    '''
    def calculate_working(self):
        contract_date=self.contract_date
        total = fields.Date.today() - date(contract_date)
        self.time_working= total.days
        return super(CollegeTeacher, self).calcule_working()
'''
    def calculate_today(self):
        self.ensure_one()
        self.last_modification = fields.Date.today()



