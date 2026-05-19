from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin = fields.Char(string="Origin")
    exw = fields.Date(string="EXW")
    stuffling = fields.Date(string="Stuffling")
    etd = fields.Date(string="ETD China/Finland")
    deliver_baku = fields.Date(string="Deliver Baku")
    
    #Actual Container qty
    ft20 = fields.Integer(string="20 ft")
    ft40 = fields.Integer(string="40 ft")
    
    # DATE (Eta Poti) / VAT (ƏDV)
    eta_poti_date = fields.Date(string="DATE (ETA Poti)")
    vat_edv = fields.Monetary(string="VAT (ƏDV)", currency_field="currency_id")
    
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        if not self.partner_ref or not self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            return res
        return {
            **res,
            'ygb_ref': self.partner_ref,
        }
