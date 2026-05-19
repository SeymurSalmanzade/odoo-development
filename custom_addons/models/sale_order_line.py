# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import format_date

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _check_company_auto = True

    lift_number = fields.Char(
        string="Number", related="product_id.lift_number")
    lift_type = fields.Char(string="Type", related="product_id.lift_type")
    lift_supply_line = fields.Char(string="Supply Line", related="product_id.lift_supply_line")
    lift_speed = fields.Float(string="Speed (m/s)",
                              related="product_id.lift_speed")
    lift_load_capacity = fields.Float(
        string="Load Capacity (kg)", related="product_id.lift_load_capacity")
    lift_floor_number = fields.Integer(
        string="Number of Floors", related="product_id.lift_floor_number")
    lift_stop_number = fields.Integer(
        string="Number of Stops", related="product_id.lift_stop_number")
    
    annex_id = fields.Many2one(
        "sale.annex", string="Annex", ondelete="restrict", copy=False, check_company=True)
    annex_assignment = fields.Char(
        related="annex_id.assignment", readonly=False)
    sequence = fields.Integer(copy=True)
    sequence2 = fields.Integer(copy=True, readonly=True, string="Sequence")
    order_date = fields.Datetime(
        related="order_id.date_order", store=True, precompute=True)
    delivery_time = fields.Char(string="Delivery Time")
    average_price_subtotal = fields.Monetary(
        string="Average", compute='_compute_average_price_subtotal', store=True, precompute=True)

    @api.depends('price_subtotal')
    def _compute_average_price_subtotal(self):
        for record in self:
            record.average_price_subtotal = record.price_subtotal

    @api.model_create_multi
    def create(self, vals):
        if 'sequence2' not in vals and 'sequence' in vals and vals['sequence']:
            vals['sequence2'] = vals['sequence']
        return super(SaleOrderLine, self).create(vals)

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            deferred_start_date = res.get('deferred_start_date')
            if deferred_start_date:
                lang = self.order_id.partner_id.lang
                formatted_date = format_date(
                    self.env, deferred_start_date, lang_code=lang, date_format='MMMM yyyy')
                res['name'] = f"{self.name}\n{formatted_date}"

        return res
