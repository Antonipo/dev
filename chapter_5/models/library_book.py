import logging

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger=logging.getLogger(__name__)


class LibraryBook(models.Model):
     _name = 'library.book.5'

     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')
     author_ids = fields.Many2many(
         'res.partner',
         string='Authors'
        )
     category_id = fields.Many2one('library.book.category.5',string='Category')
     #Defining model methods and using API decorators
     state = fields.Selection([
         ('draft', 'Unavailable'),
         ('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost'),
         ],'State',default = 'draft')
     @api.model
     def is_allowed_transitions(self,old_state ,new_state):
         allowed = [
             ('draft','available'),
             ('available','borrowed'),
             ('borrowed','available'),
             ('available','lost'),
             ('borrowed','lost'),
             ('lost','borrowed'),

            ]
         return (old_state,new_state) in allowed

     def change_state(self,new_state):
            for book in self :
                if book.is_allowed_transitions(book.state,new_state):
                    book.state = new_state
                else:
                    # Reporting errors to the user
                    msg = _('Moving from %s to %s is not allowed') % (book.state,new_state)
                    raise UserError(msg)



     def make_available(self):
         self.change_state('available')

     def make_borrowed(self):
         self.change_state('borrowed')

     def make_lost(self):
         self.change_state('lost')

#Obtaining an empty recordset for a different model

     def log_all_library_menmber(self):
         #this is an empty recordset of model library.member.5 show in the log
         library_member_model = self.env['library.member.5']
         all_member = library_member_model.search([])
         print('all members : ' , all_member)
         return True
#Creating new records
     def create_categories(self):
         categ1 = {
             'name' : 'Child category 1' ,
             'description': 'Description for child 1'
         }
         categ2 = {
             'name': 'Child category 2',
             'description': 'Description for child 2'
         }
         parent_category_val ={
             'name': 'Parent Category',
             'description': 'Description for parent category',
             'child_ids' : [
                 (0,0, categ1),
                 (0,0, categ2),

             ]
         }
         record = self.env['library.book.category.5'].create(parent_category_val)
         return True

#Updating values of recordset records
     def change_release_data(self):
         self.ensure_one()
         self.date_release = fields.Date.today()

#Searching for records
     def find_book(self):
         domain = [
             '|',
                '&',('name','ilike','Book Name'),
                    ('category_id.name','ilike','Category Name'),
                '&',('name','ilike','Book Name 2'),
                    ('category_id.name','ilike','Category Name 2')

         ]
         book= self.search(domain)
         logger.info('Books found : %s', book)
         return True

#filter recordset
     def filter_books(self):
         all_books = self.search([])
         filtered_books = self.books_with_multiple_authors(all_books)
         logger.info('Filtered books : %s',filtered_books)


     @api.model
     def books_with_multiple_authors(self,all_books):
         def predicate(book):
             if len(book.author_ids)>1:
                 return True
             return False
         res = all_books.filtered(predicate)
         print('all book filter: ', res)
         return res




class LibraryMember(models.Model):

    _name = 'library.member.5'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')








