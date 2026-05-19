from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AnnexReportWizard(models.TransientModel):
    _name = 'annex.report.wizard'
    _description = 'Annex Report Wizard'

    annex_ids = fields.Many2many("sale.annex", "print_sale_annex_ids_rel", string="Annexes to Print", help="Selected Annexes will be printed", domain="[('id','in',available_annex_ids)]")
    order_id = fields.Many2one('sale.order')
    available_annex_ids = fields.Many2many('sale.annex', compute='_compute_available_annexes', store=True)

    @api.depends('order_id.order_line')
    def _compute_available_annexes(self):
        for rec in self:
            rec.available_annex_ids = rec.order_id.order_line.mapped('annex_id')
        
    def print_annex_report(self):
        template_ref = f'custom_addons.annex_template_report'
        report_template = self.env.ref(template_ref)
        report_action = report_template.with_context(annexes=self.annex_ids.ids).report_action(self.order_id)
        report_action.update({'close_on_report_download': True})
        return report_action
    