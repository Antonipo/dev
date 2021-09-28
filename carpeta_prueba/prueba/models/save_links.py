from odoo import models,fields

class UserLink(models.Model):
    _name='user.link'
    username=fields.Char('Username')
    #favoritePag= fields.One2many('pagina.link','',String='pagina')

class PaginaLink(models.Model):
    _name='pagina.link'
    name=fields.Char('nombre')
    urlpag=fields.Char('Pagina')

class VideoUser(models.Model):
    _name='video.user'
    name=fields.Char('Title',required=True)
    description=fields.Text('Description del video')
    fecha = fields.Date('Fecha de creacion')
    username=fields.Many2one('user.link',String='usuario')
    host=fields.Many2many('pagina.link')


