from odoo import models,fields

class LibraryBook(models.Model):
     _name = 'library.book.2'
     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')
     author_ids = fields.Many2many(
         'res.partner',
         string='Authors'
        )
     #extra model definitions
     _descriptions = 'Library book'
     _order = 'date_release desc, name'
     _rec_name = 'short_name'
     short_name = fields.Char('Short Title' , required = True)

     def name_get(self):
         result = []
         for record in self:
             rec_name = "%s (%s)" % (record.name,record.date_release)
             result.append((record.id,rec_name))
             return result