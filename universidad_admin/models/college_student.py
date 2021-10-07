from odoo import fields,models


class CollegeStudent(models.Model):
    _name = 'college.student'
    name = fields.Char("Student's name" ,require=True)
    date_entry = fields.Date('Date of entry')
