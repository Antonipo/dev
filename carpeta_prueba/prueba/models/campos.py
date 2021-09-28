from odoo import models,fields,api

class fieldModel(models.Model):
    _inherit='sale.order'


    field_many2one=fields.Many2one('product.template',String='Campo Many 2 one')
    #field_one2may=fields.One2many('nuevo.model','field_many2one',String='Campo One 2 Many')