from odoo import api, fields, models # type: ignore
from datetime import timedelta
from odoo.exceptions import UserError # type: ignore
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _sql_constraints = [
        ('price', 'CHECK(price > 0)', 'Price must be greater than 0!')

    ]
    _order = "price desc"

    price = fields.Float(string = "Price")
    status = fields.Selection(string = "Status", copy = False,
                              selection = [('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string= "Partner", required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(string = "Validity (days): ", default = 7)
    date_deadline = fields.Date(string = "Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store = True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store = True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
    
    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days
            else:
                record.validity = 0

    def accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
    
    def refused(self):
        for record in self:
            record.status = 'refused'
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env['estate.property'].browse(vals['property_id'])

            if property_obj.offer_ids:
                max_offer = max(property_obj.offer_ids.mapped('price'))
                if vals['price'] < max_offer:
                    raise UserError(f"The offer must be higher than {max_offer}")

            property_obj.state = 'offer_received'

        return super().create(vals_list)