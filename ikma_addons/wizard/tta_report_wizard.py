from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class TTAReportWizard(models.TransientModel):
    _name = 'tta.report.wizard'
    _description = 'TTA Report Wizard'

    lang = fields.Selection(selection=[('az_AZ', 'AZ'),
                                       ('en_US', 'EN')], string="Language")
    date = fields.Date(string="Date", default=fields.Date.today)
    order_ids = fields.Many2many('sale.order', 'sale_order_tta_report_rel', string="Sales Orders")
    with_confirming = fields.Boolean(string="Include Executor Confirming", default=False, help="Adds the full name and position of the executor's confirming user to the report. This user is selected in the 'Contract Details' section of the Sales Order.")
    with_partner_confirming = fields.Boolean(string="Include Customer Confirming", default=False, help="Adds the full name and position of the partner’s confirming user to the report. This user is defined in the 'Contract Details' section of the Sales Order.")
    with_stamp = fields.Boolean(string="Include Stamp", default=False, help="Includes the company stamp in the report. The stamp must be set in the Company settings.")
    with_handover = fields.Boolean(string="Include Handover", default=False, help="Adds the handover person's full name and position to the report. The handover is defined in each annex.")
    with_transferee = fields.Boolean(string="Include Transferee", default=False, help="Adds the transferee's full name and position to the report. The transferee is defined in each annex.")
    without_handover_part = fields.Boolean(string="Exclude Handover Section", default=False, help="Removes both the handover and transferee sections from the report.")
    
    def print_tta_report(self):
        # Check if sale orders are selected
        if not self.order_ids:
            raise UserError(_("Please select at least one Sale Order."))
        
        for order in self.order_ids:
            order.last_updated_tta_date = self.date
            order.last_updated_tta_lang = self.lang
            
        with_context = {
            'with_confirming': self.with_confirming,
            'with_stamp': self.with_stamp,
            'without_handover_part': self.without_handover_part,
            'with_handover': self.with_handover,
            'with_transferee': self.with_transferee,
            'with_partner_confirming': self.with_partner_confirming,
            'annex_ids': self.env.context.get('annex_ids') if self.env.context.get('tta_print_from_annex') else None,
        }
        template_ref = f'ikma_addons.tta_template_report'
        report_template = self.env.ref(template_ref)
        report_action = report_template.with_context(with_context).report_action(self.order_ids)
        report_action.update({'close_on_report_download': True})
        return report_action
        