from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _check_company_auto = True

    consumption_location_id = fields.Many2one('stock.location',string="Consumption Location",index=True, domain=[('usage','=','inventory'),('scrap_location','=',True)])
    internal_location_id = fields.Many2one('stock.location',string="Internal Location",index=True, domain=[('usage','=','internal')])