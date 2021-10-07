from odoo import fields,models

class CollegeStudent(models.Model):
   _inherit = 'college.student'

   courses = fields.Many2many('course.college')


