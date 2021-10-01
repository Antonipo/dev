from odoo import models,fields,api

#copy model definition using inheritance

class LibraryBookCopy(models.Model):
    _name = 'library.book.copy'
    _inherit = 'library.book.2'
    _description = 'Library Books Copy'
