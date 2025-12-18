from odoo import api, fields, models # type: ignore
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError # type: ignore

class estateProperty(models.Model):
    _name = "estate.property"
    _description = "A real estate property demo"
    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)', 'Expected Price must be greater than 0!'),
        ('selling_price', 'CHECK(selling_price >= 0)', 'Selling Price must be positive!'),
    ]
    _order = "id desc"

    name = fields.Char(string = "Name: ", required = True)
    description = fields.Text(string = "Description: ")
    postcode = fields.Char(string = "Postcode: ")
    date_availability = fields.Date(string = "Date: ", copy = False, default= date.today() + timedelta(90))
    expected_price = fields.Float(string = "Expected Price: ", required = True)
    selling_price = fields.Float(string = "Selling Price: ", readonly = True, copy = False)
    bedrooms = fields.Integer(string = "Bedrooms: ", default = 2)
    living_area = fields.Integer(string = "Living Area: ")
    facades = fields.Integer(string = "Facades: ")
    garage = fields.Boolean(string = "Garage: ")    
    garden = fields.Boolean(string = "Garden: ")
    garden_area = fields.Integer(string = "Garden Area: ")
    garden_orientation = fields.Selection(string = "Garden Orientation: ",
                        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west','West')],
                        help = "For garden selection")
    active_selection = fields.Boolean("Active", default=True)
    state = fields.Selection(string = "State: ", default="new",
                             selection = [("new", "New"), 
                                          ("offer_received", "Offer Received"),
                                          ("offer_accepted", "Offer Accepted"),
                                          ("sold", "Sold"), ("cancelled", "Cancelled")])
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type: ")
    partner_id = fields.Many2one("res.partner", string = "Buyer")
    user_id = fields.Many2one("res.users", string = "Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(string = "Total area (sqm): ", compute = "_compute_total_area", readonly = True)
    best_price = fields.Float(string = "Best Price: ", compute = "_compute_best_price", readonly = True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            price = record.mapped("offer_ids.price")
            if price:
                record.best_price = max(price)
            else:
                record.best_price = 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = 0
                self.garden_orientation = False

    def sold_button(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("You cannot mark this property as Sold because it has been cancelled.")
            record.state = "sold"
            return True

    def cancel_button(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You cannot mark this property as Cancelled because it has been sold.")
            record.state = "cancelled"
            return True
            
    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if record.best_price < record.expected_price *  0.9 and record.selling_price > 0:
                raise ValidationError('The selling price must be at least 90% of the expected price')
            
    @api.ondelete(at_uninstall=False)
    def _unlink_except_sold_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You cannot delete a property that is not 'New' or 'Cancelled'!")