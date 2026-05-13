from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    ygb_ref = fields.Char(string="YGB Reference", copy=False)
            
    @api.onchange('partner_id')
    def _onchange_partner_id_for_internal(self):
        if self.partner_id and self.picking_type_id.code == 'internal' and self.partner_id.internal_location_id:
            self.location_dest_id = self.partner_id.internal_location_id.id
            (self.move_ids | self.move_ids_without_package).update({
                "location_id": self.location_id,
                "location_dest_id": self.partner_id.internal_location_id
            })
            
    @api.depends('name', 'ygb_ref')
    def _compute_display_name(self):
        for picking in self:
            name = picking.name
            if picking.ygb_ref:
                name += ' (' + picking.ygb_ref + ')'
            picking.display_name = name

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = args
        if name:
            domain = ['|', ('name', operator, name), ('ygb_ref', operator, name)] + args
        records = self.search(domain, limit=limit)
        return records.name_get()
    
    def name_get(self):
        result = []
        for picking in self:
            name = picking.name
            if picking.ygb_ref:
                name += ' (' + picking.ygb_ref + ')'
            result.append((picking.id, name))
        return result