from odoo import models,fields

class LibraryBook(models.Model):
     _name = 'library.book.2'
     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')

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
     cover = fields.Binary('Book Cover')
     out_of_print = fields.Boolean('Out of Print?')
     date_updated = fields.Datetime('Last Updated')
     pages = fields.Integer('Number of Pages')
     reader_rating = fields.Float(
         'Reader Average Rating',
         digits =(14,4) ,#Precision decimal
     )

     # setting float field precision with use of odoo property
     cost_price=fields.Float('Book Cost',digits='Book Price')

     #adding Monetary field
     currency_id = fields.Many2one('res.currency', String ='Currency')
     retail_price = fields.Monetary('Retail Price',
                                    #optional :Currency_field = 'currency_id'
                                    Currency_field='currency_id'
                                    )
     #adding relational fields to a model
     publisher_id = fields.Many2one(
         'res.partner', string='Publisher',
         # optional:
         ondelete='set null',
         context={},
         domain=[],
     )
     author_ids = fields.Many2many(
         'res.partner', string='Authors')

     #adding a hierarchy to a model
     category_id = fields.Many2one('library.book.category.2')

#the model class for the relational fields
class ResPartner(models.Model):
     _inherit = 'res.partner'
     published_book_ids = fields.One2many(
         'library.book.2', 'publisher_id',
         string='Published Books')
     authored_book_ids = fields.Many2many(
         'library.book.2',
         string='Authored Books',
         # relation='library_book_res_partner_rel' # optional
     )

