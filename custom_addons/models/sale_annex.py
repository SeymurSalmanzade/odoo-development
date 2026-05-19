from odoo import models, fields, api
from datetime import timedelta

class SaleAnnex(models.Model):
    _name = 'sale.annex'
    _description = 'Sale Annex'
    _check_company_auto = True

    name = fields.Char(string="Name", translate=True)
    order_id = fields.Many2one("sale.order", ondelete="cascade", check_company=True)
    order_state = fields.Selection(related="order_id.state", string="Order Status", store=True)
    order_subscription_state = fields.Selection(related="order_id.subscription_state", store=True)
    assignment = fields.Char(string="Assignment", translate=True)
    date = fields.Date(string="Annex Date")
    note_header = fields.Html(string="Header Note", default=lambda self: self.env.company.with_context(lang=self.env.user.lang).annex_note_header)
    note_footer = fields.Html(string="Footer Note", default=lambda self: self.env.company.with_context(lang=self.env.user.lang).annex_note_footer)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    
    # TTA
    tta_handover_id = fields.Many2one("res.partner", string="Handover")
    tta_handover_function = fields.Char(related="tta_handover_id.function")
    tta_transferee_id = fields.Many2one("res.partner", string="Transferee")
    tta_transferee_function = fields.Char(related="tta_transferee_id.function")
    tta_package_month_ids = fields.One2many('sale.order.tta.package.line', 'annex_id', string="Package for Months", copy=False)
                    
    def _get_package_note_for_tta_date(self, tta_date, tta_lang):
        for rec in self:
            """Fetch the package note based on the tta_date."""

            if not tta_date:
                return ''

            tta_date_obj = fields.Date.from_string(tta_date)
            tta_month = tta_date_obj.month
            tta_year = tta_date_obj.year

            # Search for the corresponding package_month_ids entry
            package_line = rec.tta_package_month_ids.filtered(
                lambda line: line.month.month == tta_month and line.month.year == tta_year
            )
            if package_line and package_line.package_id:
                return package_line.package_id.note_az if tta_lang == 'az_AZ' else package_line.package_id.note_en # Return the note of the related package
            else:
                return ''  # No package found for the given month and year

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleAnnex, self).create(vals_list)

        for record in res:  # Work on actual records, not `vals_list`
            if record.order_id and (record.order_id.state == 'sale' or record.order_id.is_existing_contract):
                contract_start_date = record.order_id.contract_start_date if not record.order_id.is_existing_contract else record.order_id.existing_contract_sale_order_id.contract_start_date
                contract_end_date = record.order_id.contract_end_date if not record.order_id.is_existing_contract else record.order_id.existing_contract_sale_order_id.contract_end_date
                if contract_start_date and contract_end_date:
                    if record.tta_package_month_ids:
                        record.tta_package_month_ids.unlink()  # Unlink existing records

                    current_date = contract_start_date
                    package_lines = []
                    while current_date <= contract_end_date:
                        package_lines.append((0, 0, {
                            'month': current_date,
                            'package_id': False,
                            'order_id': record.order_id.id
                        }))
                        # Move to the first day of the next month
                        current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
                    
                    if package_lines:
                        record.tta_package_month_ids = package_lines  # Assign new records
        return res
