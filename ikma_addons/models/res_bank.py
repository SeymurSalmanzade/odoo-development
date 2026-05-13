
from odoo import models, fields, api

class ResBank(models.Model):
    _inherit = 'res.bank'

    tax_id = fields.Char('Tax ID')
    swift = fields.Char('Swift')