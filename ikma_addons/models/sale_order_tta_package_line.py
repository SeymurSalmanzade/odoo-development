from odoo import models, fields

class SaleOrderTTAPackageLine(models.Model):
    _name = 'sale.order.tta.package.line'
    _description = 'Sale Order TTA Package Line'
    _check_company_auto = True
    
    package_id = fields.Many2one('tta.packages', string="Package", check_company=True)
    month = fields.Date(string="Month")
    order_id = fields.Many2one('sale.order', string="Order Reference", ondelete='cascade')
    annex_id = fields.Many2one('sale.annex', string="Annex Reference", ondelete='cascade')
    company_id = fields.Many2one("res.company", related="annex_id.company_id", store=True)
