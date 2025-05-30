# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BookStoreInherit(models.Model):
    _inherit = 'book_store.book_store'

   
    seller_company = fields.Many2one('mb_companies', default=lambda self: self._get_default_seller_company())
    @api.model
    def _get_default_seller_company(self):
        default_company = self.env['mb_companies'].search([('name', '=', 'Erpgo')], limit=1)
        return default_company.id if default_company else False


