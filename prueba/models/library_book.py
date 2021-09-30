from odoo import models,fields,api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name ='library.book'
    name = fields.Char('Title', required=True)
    #date_release = fields.Date('Release Date')

    #detect duplicate part at server database
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)',
         'No of pages must be positive')
    ]
    #detect duplicate part at server level
    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    author_ids = fields.Many2many(
        'res.partner', string='Authors')

    #in this part call a external model
    category_id = fields.Many2one('library.book.category')

    #limiting acess in model with rol
    is_public = fields.Boolean(groups='prueba.group_library_librarian')
    private_notes = fields.Text(groups='prueba.group_library_librarian')

    #Using security groups to activate features
    date_release = fields.Date('Release Date',groups='prueba.group_release_dates')

    #only accessed as a superuser
    report_missing = fields.Text(
        String = "Book is missing",
        groups = 'prueba.group_library_librarian',
    )

    def report_missing_book(self):
        self.ensure_one()
        message = "Book is missing (Reported by: %s)" % self.env.user.name
        self.sudo().write({
            'report_missing' : message
        })



class ResPartner(models.Model):
     _inherit = 'res.partner'
     published_book_ids = fields.One2many(
     'library.book', 'publisher_id',
     string='Published Books')
     authored_book_ids = fields.Many2many(
     'library.book',
     string='Authored Books',
     # relation='library_book_res_partner_rel' #
     )



