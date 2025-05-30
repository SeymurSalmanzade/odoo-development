# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResBankInherit(models.Model):
    _inherit = 'res.bank'

    tax_id = fields.Char('Tax ID')
    swift = fields.Char('Swift')

class ResPartnerBankInheerit(models.Model):
    _inherit = 'res.partner.bank'

    muxbir_hesab = fields.Char('C/A', help="Correspondent Account(Müxbir/Hesab)")

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     brand = fields.Char('Brand', required= True)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    ship_by = fields.Char('Ship By')


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    director = fields.Char('Director')
    director_sign = fields.Binary('Sign')
    stamp = fields.Binary('Stamp')