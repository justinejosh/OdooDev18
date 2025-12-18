from odoo import models, fields #type: ignore

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    property_ids = fields.One2many(
        'estate.property', 
        'user_id', 
        string='Properties',
        domain=[('state', 'not in', ['sold', 'cancelled'])]
    )