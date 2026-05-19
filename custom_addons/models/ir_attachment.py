from odoo import models, fields

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    sequence = fields.Integer(default=10)
    