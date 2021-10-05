import logging

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger=logging.getLogger(__name__)


class LibraryBook(models.Model):
     _name = 'library.book.5'

     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')

     category_id = fields.Many2one('library.book.category.5',string='Category')

     pages = fields.Integer('Number of Pages')
     cost_price = fields.Float('Book Cost')


     def grouped_data(self):
         data = self._get_average_cost()
         _logger.info("Groupped Data : %s"% data)


     @api.model
     def _get_average_cost(self):
         grouped_result = self.read_group(
             [('cost_price', "!=",False)],#domain
             ['category_id', 'cost_price:avg'],#fields to access
             ['category_id'],#group_by
         )
         return grouped_result



     #Customizing how records are searched
     isbn = fields.Char('ISBN')
     author_ids = fields.Many2many(
         'res.partner',
         string='Authors'
     )

     #Customizing how records are searched
     def  name_get(self):
         result = []
         for book in self:
             authors = book.author_ids.mapped('name')
             name = '%s (%s)' % (book.name , ', '.join(authors))
             result.append((book.id,name))
             return result
     @api.model
     def _name_search(self,name ='', args=None , operator = 'ilike',limit = 100 , name_get_uid = None):
         args = [] if args is None else args.copy()
         if not (name == '' and operator == 'ilike'):
             args += [ '|','|',
                       ('name',operator,name),
                       ('isbn',operator,name),
                       ('author_ids.name',operator,name),
             ]
         return super(LibraryBook,self)._name_search(
             name = name ,args = args,operator =operator,
             limit = limit, name_get_uid=name_get_uid
         )
     old_editions = fields.Many2one('library.book.5', string='Old Edition')

#Extending write() and create()
     manager_remarks = fields.Text('Manager Remarks')

     @api.model
     def create(self,values):
         if not self.user_has_groups('chapter_5.group_librarian_5'):
             if 'manager_remarks' in values:
                 raise UserError (
                     'You are not allowed to modify'
                     'manager_remarks'
                 )
         return super(LibraryBook,self).create(values)
     def write(self, values):
         if not self.user_has_groups('chapter_5.group_librarian_5'):
             if 'manager_remarks' in values:
                 raise UserError (
                     'You are not allowed to modify'
                     'manager_remarks'
                 )
         return  super(LibraryBook,self).write(values)





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
         _logger.info('Books found : %s', book)
         return True

#filter recordset
     def filter_books(self):
         all_books = self.search([])
         filtered_books = self.books_with_multiple_authors(all_books)
         _logger.info('Filtered books : %s',filtered_books)


     @api.model
     def books_with_multiple_authors(self,all_books):
         def predicate(book):
             if len(book.author_ids)>1:
                 return True
             return False
         res = all_books.filtered(predicate)
         print('all book filter: ', res)
         return res

     # traversing recordset relations
     def mapped_books(self):
         all_books = self.search([])
         books_authors = self.get_author_names(all_books)
         _logger.info('Books Authors :' , books_authors)

     @api.model
     def get_author_names(self,books):
         return books.mapped('author_ids.name')

#Sorting recordsets
     def sorted_books(self):
         all_books = self.search([])
         book_sorted = self.sort_books_by_date(all_books)
         _logger.info('Book before sorting : ' , all_books)
         _logger.info('Book after sorting : ' , book_sorted)

     @api.model
     def sort_books_by_date(self,books):
         return books.sorted(key='date_release')




class LibraryMember(models.Model):

    _name = 'library.member.5'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')








