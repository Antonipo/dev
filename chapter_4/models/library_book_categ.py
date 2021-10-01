from odoo import models, fields, api
from odoo.exceptions import ValidationError

#the model that will be the hierarchy
class BookCategory(models.Model):
       _name = 'library.book.category.2'
       name = fields.Char('Category')
       parent_id = fields.Many2one(
           'library.book.category.2',
           string='Parent Category',
           ondelete='restrict',
           index=True)
       child_ids = fields.One2many(
        'library.book.category.2', 'parent_id',
        string='Child Categories')

       #for enable the special hierarchy support (parent)
       _parent_store = True
       _parent_name = 'parent_id'
       parent_path = fields.Char(index = True)

       @api.constrains('parent_id')
       def _check_hierarchy(self):
           if not self._check_recursion():
               raise models.ValidationsError(
                   'Error! You can not create recursive category.'
               )
