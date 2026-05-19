from odoo import models, fields

class HrLeave(models.Model):
    _name = 'hr.leave'
    _inherit = ['hr.leave', 'custom.common']
    
    working_year_from = fields.Date(string="Working Year From")
    working_year_to = fields.Date(string="Working Year To")
    working_start_date = fields.Date(string="Working Start Date")
    order_number = fields.Char(string="Order Number")
    order_date = fields.Date(string="Order Date", default=fields.Date.context_today)
    businness_trip_location = fields.Char(string="Business Trip Location")
    