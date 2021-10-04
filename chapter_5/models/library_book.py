from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class LibraryBook(models.Model):
     _name = 'library.book.5'

     name = fields.Char('Title', required=True)
     date_release = fields.Date('Release Date')
     author_ids = fields.Many2many(
         'res.partner',
         string='Authors'
        )
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



class LibraryMember(models.Model):

    _name = 'library.member.5'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')








