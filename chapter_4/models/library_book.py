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

    #this is for the page tag
     def name_get(self):
         result = []
         for record in self:
             rec_name = "%s (%s)" % (record.name,record.date_release)
             result.append((record.id,rec_name))
             return result

     #adding data fields to a model
     notes = fields.Text('Internal Notes')
     state = fields.Selection(
             [
                 ('draft', 'Not Avalible'),
                 ('avalible','Avalible'),
                 ('lost','Lost'),
             ],'State'
         )
     descriptions = fields.Html('Descriptions')
     cover = fields.Boolean('Book Cover')
     out_of_print = fields.Boolean('Out of Print?')
     date_updated = fields.Datetime('Last Updated')
     pages = fields.Integer('Number of Pages')
     reader_rating = fields.Float(
         'Reader Average Rating',
         digits =(14,4) ,#Precision decimal

     )