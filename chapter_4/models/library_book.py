from odoo import models,fields,api
from datetime import timedelta


#Using abstract models for reusable model features
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Abstract Archive'

    active = fields.Boolean(default=True)


    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
     _name = 'library.book.2'
     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')

     # Using abstract models for reusable model features
     _inherit = ['base.archive']

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

     # validations constraint to a model

     # checked at the database level
     _sql_constraints = [
         ('name_uniq', 'UNIQUE (name)',
          'Book title must be unique.'),
         ('positive_page', 'CHECK(pages>0)',
          'No of pages must be positive')
         #another example
         #('check_credit_debit',
         # 'CHECK(credit + debit>=0 AND credit * debit=0)',
         # 'Wrong credit or debit value in accounting entry!'
         # )
     ]

     # checked at the server level
     @api.constrains('date_release')
     def _check_release_date(self):
         for record in self:
             if record.date_release and record.date_release > fields.Date.today():
                 raise models.ValidationError('Release date must be in the past')

     #Adding computed fields to a model
     age_days = fields.Float(
            string = 'Days Since Release',
            compute = '_compute_age',
            inverse = '_inverse_age',
            search = '_search_age',
            #store = False , optional
            #compute_sudo = True, optional
        )
     @api.depends('date_release')
     def _compute_age(self):
         today = fields.Date.today()
         for book in self:
             if book.date_release:
                 delta = today- book.date_release
                 book.age_days = delta.days
             else:
                book.age_days=0
     def _inverse_age(self):
         today = fields.Date.today()
         for book in self.filtered('date_release'):
             d= today - timedelta(days = book.age_days)
             book.date_release = d
     def _search_age(self,operator,value):
         today = fields.Date.today()
         value_days = timedelta(days =value)
         value_date = today - value_days
         #convert the operator :
         #book whit age> value have a date < values_date
         operator_map = {
             '>' : '<' ,'>=' : '<=',
             '<' : '>', '<=': '>='
         }
         new_op = operator_map.get(operator,operator)
         return [('date_release',new_op,value_date)]

     #exposing related fields stored in other models
     publisher_city = fields.Char(
         'Publisher City',
         related = 'publisher_id.city',
         readonly = True
     )

     #adding dynamic relations using referenc fields
     ref_doc_id = fields.Reference(
         selection = '_referencable_models',
         string = 'Reference Document'
     )

     @api.model
     def _referencable_models(self):
         models = self.env['ir.model'].search([
             ('field_id.name', '=' , 'message_ids')
         ])
         return [(x.model ,x.name) for x in models]









#the model class for the relational fields
class ResPartner(models.Model):
     _inherit = 'res.partner'
     published_book_ids = fields.One2many(
         'library.book.2', 'publisher_id',
         string='Published Books')

     # adding features to a model using inheritances

     # class inheritances (extension)
     authored_book_ids = fields.Many2many(
         'library.book.2',
         string='Authored Books',
         # relation='library_book_res_partner_rel' # optional
     )
     count_books = fields.Integer('Number of authored Books',
                                  compute= '_compute_count_book'
                                  )
     @api.depends('authored_book_ids')
     def _compute_count_book(self):
         for r in self:
             r.count_book = len(r.authored_book_ids)


#Using delegation inheritance to copy features to another model

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner' : 'partner_id'}#tthis can be removed by adding to the following command this "delegate = True "
    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade'
    )
    data_start = fields.Date('Member Since')
    data_end = fields.Date('Termination Date')
    member_number = fields.Char()
    data_of_birth = fields.Date('Data of birth')

