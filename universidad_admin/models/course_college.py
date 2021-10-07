from odoo import models,fields


class CourseCollege(models.Model):
    _name = 'course.college'
    name = fields.Char('Course name : ',require=True)
    faculty = fields.Selection(
        [
            ('default','Select'),
            ('engineering','Faculty of Engineering'),
            ('law','Law School'),
            ('science','Science Faculty'),
            ('economy','Economy Faculty'),
        ],'Faculty',default = 'default'
    )
    teacher = fields.Many2one('college.teacher','Teacher')

