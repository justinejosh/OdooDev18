from odoo import api, fields, models # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _sql_constraints = [
        ('name', 'UNIQUE(name)', "Property Type must be unique!")
    ]
    _order = "sequence, name" 

    name = fields.Char("Property Type: ", required = True)
    property_ids = fields.One2many("estate.property", "property_type_id", readonly = True)
    sequence = fields.Integer("Sequence", default = 1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string = "Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)