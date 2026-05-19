
from odoo import models, fields, api

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    muxbir_hesab = fields.Char('C/A', help="Correspondent Account(Müxbir/Hesab)")
    correspondent_bank_name = fields.Char(string='C/B', help="Correspondent Bank(Müxbir/Bank)")
    correspondent_bank_swift = fields.Char(string='C/B Swift', help="Correspondent Bank Swift(Müxbir/Bank swift)")
    bank_swift = fields.Char(related="bank_id.swift")
    bank_tax_id = fields.Char(related="bank_id.tax_id")