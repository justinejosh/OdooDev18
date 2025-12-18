from odoo import fields, models # type: ignore

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Property Tag must be unique!')
    ]
    _order = "name"
    
    name = fields.Char("Name: ", required = True)
    color = fields.Integer()