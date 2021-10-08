from odoo import models,fields,api
import datetime



class CollegeTeacher(models.Model):
    _name = 'college.teacher'
    name = fields.Char('Name Teacher :',required=True )
    contract_date = fields.Date(string='Contrac Date')
    time_working= fields.Char('Time Working',compute='_get_age',readonly= True)
    defined_contract = fields.Boolean('Defined Contract',groups='universidad_admin.group_college_principal')
    last_modification = fields.Date('last Modification',readonly = True)



    @api.onchange('contract_date')
    def _get_age(self):
        print('entrooooo')
        if self.contract_date:
            date1=self.contract_date
            old_year= date1.strftime('%Y')
            today_age = datetime.datetime.now()
            date = today_age.date()
            now_year=date.strftime('%Y')
            total=int(now_year)-int(old_year)
            self.time_working=str(total)+' years working'




    def calculate_today(self):
        self.ensure_one()
        self.last_modification = fields.Date.today()



