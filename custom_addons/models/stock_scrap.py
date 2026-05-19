from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    partner_id = fields.Many2one('res.partner',string='Contact', index=True, domain=[('is_company','=',False)])

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            if rec.partner_id and rec.partner_id.consumption_location_id:
                rec.scrap_location_id = rec.partner_id.consumption_location_id.id
