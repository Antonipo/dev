from odoo import models,fields,api


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



    def name_get(self):
        result = []
        for course in self:
            teacher = course.teacher.mapped('name')
            name = '%s (%s)' % (course.name, ', '.join(teacher))
            result.append((course.id, name))
            return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('isbn', operator, name),
                     ('teacher.name', operator, name),
                     ]
        return super(CourseCollege, self)._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid
            
        )


