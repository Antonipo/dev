from odoo import models,fields,api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name ='library.book'
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
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
    category_id = fields.Many2one('library.book.category')

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


