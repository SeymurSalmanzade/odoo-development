# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from itertools import chain

SALE_CONTRACT_TYPE = {
    'none': _('None'),
    'service': _('Service'),
    'installation': _('Installation'),
    'supply': _('Supply'),
    'spare_parts': _('Spare Parts'),
    'turnkey': _('Turnkey'),
    'spo': _('SPO'),
}

SALE_SERVICE_ADDENDUM_TYPE = {
    'base': _('Base'),
    'standard': _('Standard'),
    'premium': _('Premium'),
    'premium_plus': _('Premium +')
}

SALE_INSTALLATION_ADDENDUM_TYPE = {
    'obligations': _('Obligations'),
}

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'custom.common']
    _check_company_auto = True
    
    amount_per_line = fields.Monetary(string="Amount Per Line", compute="_compute_amount_per_line", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    recurring_per_line = fields.Monetary(string="Recurring Per Line", compute="_compute_recurring_per_line", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    is_individual_partner = fields.Boolean(string="Individual Customer", compute="_compute_is_individual_partner", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    is_custom_contract_user = fields.Boolean(string="CUSTOM Contract User", compute="_compute_is_custom_contract_user")
    opportunity_no = fields.Char(string="Opportunity Number", related='opportunity_id.opportunity_no')
    header_contract_attachment_ids = fields.Many2many("ir.attachment", "sale_order_header_contract_attachment_rel", string="Header Attachments")
    footer_contract_attachment_ids = fields.Many2many("ir.attachment", "sale_order_footer_contract_attachment_rel", string="Footer Attachments")
    is_approved_quotation = fields.Boolean(string="Approved Quotation", default=False)
    
    # Main Details
    is_existing_contract = fields.Boolean(string="Existing Contract", default=False)
    existing_contract_sale_order_id = fields.Many2one("sale.order", string="Related Sale Order", ondelete="restrict", help="Existing Contract's Sale Order")
    signed_contract = fields.Boolean(string="Signed Contract", default=False, copy=False)
    contract_type = fields.Selection(selection=[
        *SALE_CONTRACT_TYPE.items()], string="Contract Type")
    contract_template_id = fields.Many2one("sale.contract.template", string="Contract Template", check_company=True)
    service_addendum = fields.Selection(selection=[
        *SALE_SERVICE_ADDENDUM_TYPE.items()], string="Addendum Type")
    installation_addendum = fields.Selection(selection=[
        *SALE_INSTALLATION_ADDENDUM_TYPE.items()], string="Addendum Type")
    installation_total_price = fields.Monetary(string="Installation Total Price")
    addendum_template_id = fields.Many2one("sale.addendum.template", string="Addendum Template", check_company=True)
    contract_number = fields.Char(string="Contract Number")
    project_number = fields.Char(string="Project Number")
    project_name = fields.Char(string="Project Name", compute="_compute_project_name", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    contract_date = fields.Date(string="Contract Date")
    contract_partner_company = fields.Many2one("res.partner", string="Customer Company", compute="_compute_contract_partner_company", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    contract_partner_company_short = fields.Char(string="Customer Company Short")
    contract_partner_person = fields.Many2one("res.partner", string="Customer Person")
    contract_partner_person_position = fields.Char(string="Customer Person Position", related="contract_partner_person.function")
    contract_executor_person = fields.Many2one("res.partner", string="Executor Person")
    contract_executor_person_position = fields.Char(string="Executor Person Position", related="contract_executor_person.function")
    contract_current_address = fields.Char(string="Current Address")
    
    # Order Line Sequence
    max_line_sequence = fields.Integer(string='Max sequence in lines')
    max_line_sequence2 = fields.Integer(string='Max sequence in lines Show')

    # Customer requisites
    partner_recipient_bank_id = fields.Many2one('res.partner.bank', string="Customer Recipient Bank")
    contract_partner_address = fields.Char(string="Customer Address", related="contract_partner_company.contact_address_complete")
    contract_partner_tin = fields.Char(string="Customer TIN", related="contract_partner_company.vat")
    contract_partner_bank_acc_number = fields.Char(string="Customer Account Number", related="partner_recipient_bank_id.acc_number")
    contract_partner_correspondent_acc_number = fields.Char(string="Customer C/A Number", related="partner_recipient_bank_id.muxbir_hesab")
    contract_partner_bank_swift = fields.Char(string="Customer Bank SWIFT", related="partner_recipient_bank_id.bank_swift")
    contract_partner_bank_tin = fields.Char(string="Customer Bank TIN", related="partner_recipient_bank_id.bank_tax_id")
    contract_partner_bank_code = fields.Char(string="Customer Bank Code", related="partner_recipient_bank_id.bank_bic")
    contract_partner_bank_name = fields.Char(string="Customer Bank Name", related="partner_recipient_bank_id.bank_name")
    
    # Individual Customer requisites
    contract_partner_birthday = fields.Date(string="Customer Birthday")
    contract_partner_passport_serial_number = fields.Char(string="Customer Passport S/N")
    contract_partner_passport_fin = fields.Char(string="Customer Passport FIN")
    
    # Executor requisites
    company_partner_id = fields.Many2one('res.partner', related="company_id.partner_id")
    company_recipient_bank_id = fields.Many2one('res.partner.bank', string="Executor Recipient Bank")
    contract_executor_address = fields.Char(string="Executor Address", related='company_id.street')
    contract_executor_tin = fields.Char(string="Executor TIN", related='company_id.vat')
    contract_executor_bank_acc_number = fields.Char(string="Executor Account Number", related='company_recipient_bank_id.acc_number')
    contract_executor_correspondent_acc_number = fields.Char(string="Executor C/A Number", related='company_recipient_bank_id.muxbir_hesab')
    contract_executor_bank_swift = fields.Char(string="Executor Bank SWIFT", related='company_recipient_bank_id.bank_swift')
    contract_executor_bank_tin = fields.Char(string="Executor Bank TIN", related='company_recipient_bank_id.bank_tax_id')
    contract_executor_bank_code = fields.Char(string="Executor Bank Code", related='company_recipient_bank_id.bank_bic')
    contract_executor_bank_name = fields.Char(string="Executor Bank Name", related='company_recipient_bank_id.bank_name')

    # TTA
    last_updated_tta_date = fields.Date(string="Last Updated TTA Date")
    last_updated_tta_lang = fields.Selection(selection=[('az_AZ','AZ'),
                                                        ('en_US','EN')], string="Last Updated TTA Lang")
    contract_start_date = fields.Date(string="Müqavilə Başlama", store=True, copy=False)
    contract_end_date = fields.Date(string="Müqavilə Bitmə", store=True, copy=False)
    tta_confirming_user_id = fields.Many2one('res.users', string="Təsdiq Edən İcraçı")
    tta_confirming_user_function = fields.Char(related="tta_confirming_user_id.function", string="İcraçı Vəzifə")
    tta_confirming_partner_id = fields.Many2one('res.partner', string="Təsdiq Edən Müştəri")
    tta_confirming_partner_function = fields.Char(related="tta_confirming_partner_id.function", string="Müştəri Vəzifə")
    tta_attachment_ids = fields.Many2many("ir.attachment", "sale_order_tta_attachment_rel", string="TTA Attachments")
    has_tta_attachments = fields.Boolean(string="Has TTA", compute="_compute_has_tta_attachments", store=True, groups="custom_addons.group_custom_azerbaijan_user")
    
    # Annex
    annex_ids = fields.One2many("sale.annex", "order_id", string="Related Annexes")
    annex_tax_totals = fields.Binary(compute="_compute_annex_tax_totals", groups="custom_addons.group_custom_azerbaijan_user")
    
    # Commercial Offer
    spo_note = fields.Html(string="SPO Note", help="Additional note for SPO (Commercial Offer)", default=lambda self: self.env.company.with_context(lang=self.env.user.lang).spo_note)
    spo_date = fields.Date(string="SPO Date", help="Date of the SPO (Commercial Offer)", default=fields.Date.today)
    spo_count = fields.Integer(string="SPO Count", compute="_compute_spo_count", groups="custom_addons.group_custom_azerbaijan_user", help="Number of SPO (Commercial Offers) related to this order")
    
    @api.depends('tta_attachment_ids')
    def _compute_has_tta_attachments(self):
        for rec in self:
            rec.has_tta_attachments = bool(rec.tta_attachment_ids)
            
    @api.depends('order_line')
    def _compute_project_name(self):
        for record in self:
            order_line = record.order_line.filtered(lambda l: not l.display_type)
            if order_line:
                record.project_name = order_line[0].annex_assignment
                
    def _compute_spo_count(self):
        for order in self:
            order.spo_count = self.env["sale.order"].search_count([('is_existing_contract', '=', True), ('existing_contract_sale_order_id', '=', order.id), ('contract_type', '=', 'spo')])
            
    def action_view_related_spo_orders(self):
        self.ensure_one()
        return {
            'name': _('Related SPO Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('is_existing_contract', '=', True), ('existing_contract_sale_order_id', '=', self.id), ('contract_type', '=', 'spo')],
        }
        
    def approve_quotation(self):
        for order in self:
            if not order.is_approved_quotation:
                order.is_approved_quotation = True
                
    @api.constrains('header_contract_attachment_ids', 'footer_contract_attachment_ids')
    def _check_contract_attachments_is_pdf(self):
        for order in self:
            all_attachments = chain(order.header_contract_attachment_ids, order.footer_contract_attachment_ids)
            if any(att.type != 'binary' or att.mimetype != 'application/pdf' for att in all_attachments):
                raise ValidationError(_("Only PDF attachments are allowed for contract headers and footers."))
            
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['is_custom_contract_user'] = self.env.user.has_group('custom_addons.group_custom_azerbaijan_user')
        return res
    
    @api.onchange('is_existing_contract')
    def _onchange_is_existing_contract(self):
        for rec in self:
            if rec.is_existing_contract:
                rec.contract_type = 'spo'
            else:
                rec.contract_type = False

    @api.onchange('is_existing_contract', 'existing_contract_sale_order_id')
    def _onchange_existing_contract(self):
        for rec in self:
            if rec.is_existing_contract and rec.existing_contract_sale_order_id:
                rec.project_number = rec.existing_contract_sale_order_id.project_number
                
    @api.onchange('service_addendum', 'installation_addendum', 'contract_type')
    def _onchange_addendum_type(self):
        for rec in self:
            rec.addendum_template_id = False
        
    @api.onchange('contract_type')
    def _onchange_contract_type(self):
        for rec in self:
            rec.contract_template_id = False
            rec.service_addendum = False
            rec.installation_addendum = False
            if rec.contract_type == 'spo':
                rec.is_existing_contract = True
        
    @api.onchange('contract_number')
    def _onchange_contract_number(self):
        if self.contract_number:
            self.client_order_ref = "Müqavilə № " + self.contract_number
        
    def _compute_is_custom_contract_user(self):
        custom_contract_user = self.env.user.has_group('custom_addons.group_custom_azerbaijan_user')
        for rec in self:
            rec.is_custom_contract_user = custom_contract_user
            
    @api.depends('partner_id')
    def _compute_is_individual_partner(self):
        for rec in self:
            if rec.partner_id and not rec.partner_id.is_company and not rec.partner_id.parent_id:
                rec.is_individual_partner = True
            else:
                rec.is_individual_partner = False
                
    @api.depends('order_line', 'amount_total')
    def _compute_amount_per_line(self):
        """Compute the amount per line based on the order lines."""
        for rec in self:
            valid_lines = rec.order_line.filtered(lambda line: not line.display_type)
            rec.amount_per_line = rec.amount_total / len(valid_lines) if rec.amount_total > 0 and rec.order_line else 0.0
    
    @api.depends('order_line', 'recurring_total')
    def _compute_recurring_per_line(self):
        """Compute the recurring amount per line based on the order lines."""
        for rec in self:
            valid_lines = rec.order_line.filtered(lambda line: not line.display_type)
            rec.recurring_per_line = rec.recurring_total / len(valid_lines) if rec.recurring_total > 0 and rec.order_line else 0.0
            
    @api.depends('order_line','order_line.annex_id')
    def _compute_annex_ids(self):
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            for rec in self:
                rec._get_annexes_with_related_order()
            
    @api.depends('partner_id')
    def _compute_contract_partner_company(self):
        for rec in self:
            if not rec.partner_id.is_company and rec.partner_id.parent_id:
                rec.contract_partner_company = rec.partner_id.parent_id.id
            else:
                rec.contract_partner_company = rec.partner_id.id
                    
    def _validate_contract_state(self):
        state = dict(self._fields['state'].selection).get(self.state)
        if self.state in ('sale', 'cancel'):
            raise UserError(_("You cannot change the Contract status in this state: %s. If you need to change status, Set to Quotation.") % state)
        return True
            
    def _check_empty_fields(self):
        empty_fields = []
        required_fields = [
            'contract_type', 'contract_template_id', 'contract_number', 'project_number',
            'contract_date', 'contract_partner_company', 'contract_partner_company_short',
            'contract_partner_person', 'contract_partner_person_position',
            'contract_executor_person', 'contract_executor_person_position', 'contract_current_address',
            'contract_partner_address',
            'company_recipient_bank_id', 'contract_executor_address',
            'contract_executor_tin', 'contract_executor_bank_acc_number', 
            'contract_executor_correspondent_acc_number', 'contract_executor_bank_swift',
            'contract_executor_bank_tin', 'contract_executor_bank_code', 
            'contract_executor_bank_name', 'contract_start_date', 'contract_end_date'
        ]
        
        if not self.is_individual_partner:
            required_fields.extend([
                'contract_partner_tin',
                'partner_recipient_bank_id',
                'contract_partner_bank_acc_number',
                'contract_partner_correspondent_acc_number',
                'contract_partner_bank_swift',
                'contract_partner_bank_tin',
                'contract_partner_bank_code',
                'contract_partner_bank_name',
            ])
        else:
            required_fields.extend([
                'contract_partner_birthday',
                'contract_partner_passport_serial_number',
                'contract_partner_passport_fin',
            ])
            
        if self.contract_type in ('service', 'installation'):
            if self.contract_type == 'service':
                required_fields.append('service_addendum')
            else:
                required_fields.append('installation_addendum')
            required_fields.append('addendum_template_id')
            
        for field_name in required_fields:
            if not getattr(self, field_name, False):
                field = self._fields.get(field_name)
                if field and field.string:
                    empty_fields.append(f"*{field.string}*")

        if empty_fields:
            field_names = '\n'.join(empty_fields)
            raise UserError(_('⚠️ Please fill the following fields before proceeding:\n\n%s') % field_names)

        return True
        
    def sign_contract(self):
        valid_state = self._validate_contract_state()
        if valid_state:
            self._check_empty_fields()
            if not self.signed_contract:
                self.signed_contract = True

    def cancel_contract(self):
        self._validate_contract_state()
        if self.signed_contract:
            self.signed_contract = False
            
    def _get_annexes_with_related_order(self):
        """Retrieve all annexes related to the current order."""
        return self.env['sale.annex'].search([('order_id','=',self.id)])
    
    def _get_annexes_in_order_line(self):
        return self.order_line.mapped('annex_id')
    
    def _get_annex_order_lines(self, annex):
        """Retrieve displayable order lines for the specified annex, 
        considering downpayment display rules.
        """
        def is_displayable_line(line, downpayment_lines):
            """Determine if the line should be shown."""
            if not line.is_downpayment:
                return True
            if line.display_type and downpayment_lines:
                return True
            if line in downpayment_lines:
                return True
            return False
        
        # Get all displayable downpayment lines (posted downpayments)
        downpayment_lines = self.order_line.filtered(
            lambda line: line.is_downpayment and not line.display_type and not line._get_downpayment_state()
        )

        # Filter order lines belonging to the specified annex and are displayable
        return self.order_line.filtered(
            lambda line: line.annex_id == annex and is_displayable_line(line, downpayment_lines)
        )

    @api.depends_context('lang')
    @api.depends('order_line.price_subtotal', 'currency_id', 'company_id', 'payment_term_id')
    def _compute_annex_tax_totals(self):
        """Compute and assign tax totals for each annex in the order."""

        def compute_tax_totals_for_lines(order, line_filter):
            """Helper to compute tax totals for given filtered lines."""
            AccountTax = self.env['account.tax']
            order_lines = order.order_line.filtered(line_filter)
            base_lines = [line._prepare_base_line_for_taxes_computation() for line in order_lines]
            base_lines += order._add_base_lines_for_early_payment_discount()
            AccountTax._add_tax_details_in_base_lines(base_lines, order.company_id)
            AccountTax._round_base_lines_tax_details(base_lines, order.company_id)
            return AccountTax._get_tax_totals_summary(
                base_lines=base_lines,
                currency=order.currency_id or order.company_id.currency_id,
                company=order.company_id,
            )

        for order in self:
            annex_totals = {}
            annexes = order._get_annexes_in_order_line()

            for annex in annexes:
                annex_totals[annex.id] = compute_tax_totals_for_lines(
                    order,
                    line_filter=lambda line: not line.display_type and line.annex_id == annex
                )

            order.annex_tax_totals = annex_totals
           
    def _reset_sequence(self):
        for rec in self:
            company = rec.company_id
            current_sequence = 1
            current_sequence2 = 1
            for line in rec.order_line.sorted(lambda r: r.sequence):
                line.write({
                    'sequence': current_sequence,
                    'sequence2': current_sequence2,
                })
                current_sequence += 1
                if company.sale_line_sequence_product_only and line.display_type:
                    pass
                else:
                    current_sequence2 += 1
            rec.write({
                'max_line_sequence': current_sequence - 1,
                'max_line_sequence2': current_sequence2 - 1,
            })

    def _prepare_upsell_renew_order_values(self, subscription_state):
        values = super()._prepare_upsell_renew_order_values(subscription_state)
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            additional_values = {
                'is_existing_contract': self.is_existing_contract,
                'existing_contract_sale_order_id': self.existing_contract_sale_order_id.id,
                'contract_type': self.contract_type,
                'contract_template_id': self.contract_template_id.id,
                'service_addendum': self.service_addendum,
                'installation_addendum': self.installation_addendum,
                'addendum_template_id': self.addendum_template_id.id,
                'contract_number': self.contract_number,
                'project_number': self.project_number,
                'contract_date': self.contract_date,
                'contract_partner_company_short': self.contract_partner_company_short,
                'contract_partner_person': self.contract_partner_person.id,
                'contract_executor_person': self.contract_executor_person.id,
                'contract_current_address': self.contract_current_address,
                'partner_recipient_bank_id': self.partner_recipient_bank_id.id,
                'company_recipient_bank_id': self.company_recipient_bank_id.id,
                'tta_confirming_user_id': self.tta_confirming_user_id.id,
            }

            values.update(additional_values)
        return values
    
    def _update_renew_upsell_order_line_annex_values(self, order):
        processed_annexes = {}
        for line in order.order_line:
            if line.parent_line_id and line.parent_line_id.annex_id:
                annex_id = line.parent_line_id.annex_id.id
                if annex_id not in processed_annexes:
                    new_annex = line.parent_line_id.annex_id.copy({
                        'order_id': order.id,
                        'date': order.date_order,
                    })
                    processed_annexes[annex_id] = new_annex
                else:
                    new_annex = processed_annexes[annex_id]
                line.annex_id = new_annex
              
    def _create_renew_upsell_order(self, subscription_state, message_body):
        order = super()._create_renew_upsell_order(subscription_state, message_body)
        if order and self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            order._update_renew_upsell_order_line_annex_values(order)
        return order
    
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        recal = False
        if vals.get('order_line') and vals['order_line']:
            for line in vals['order_line']:
                if line[0] == 0 and 'sequence' in line[2]:  # Create
                    recal = True
                    break
                elif line[0] == 1 and line[2] and 'sequence' in line[2]:  # Update
                    recal = True
                    break
                elif line[0] == 2:  # Delete
                    recal = True
                    break
        if recal:
            for rec in self:
                rec._reset_sequence()
                pass
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)

        # Iterate over both vals_list and res to match them
        for record, vals in zip(res, vals_list):
            if 'order_line' in vals and vals['order_line']:
                record._reset_sequence()
            if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
                if 'opportunity_id' in vals and vals['opportunity_id']:
                    opportunity = self.env['crm.lead'].browse(vals['opportunity_id'])
                    if opportunity and opportunity.opportunity_no != _('New'):
                        # Safely split and reconstruct name
                        name_parts = record.name.split('-')
                        if len(name_parts) > 1:
                            first_part = name_parts[:-1]
                            last_part = name_parts[-1]
                            prefix = opportunity.opportunity_no.split('-')[-2:-1]
                            record.name = f"{'-'.join(first_part)}-{'-'.join(prefix)}-{last_part}"
        return res

    def action_confirm(self):
        """Overrides the confirmation action to update the order name with contract prefixes and generate package months for each annex."""
        res = super().action_confirm()
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            for rec in self:
                project_number = rec.project_number if not rec.is_existing_contract else rec.existing_contract_sale_order_id.project_number
                signed_contract = rec.signed_contract if not rec.is_existing_contract else rec.existing_contract_sale_order_id.signed_contract
                contract_prefix = ""
                if project_number and signed_contract and (rec.contract_type not in ('none', False) or rec.is_existing_contract):
                    contract_prefix = rec._get_contract_prefix(contract_type=rec.contract_type, project_number=project_number)

                if contract_prefix:
                    rec._update_order_name(contract_prefix)

                contract_start_date = self.contract_start_date if not self.is_existing_contract else self.existing_contract_sale_order_id.contract_start_date
                contract_end_date = self.contract_end_date if not self.is_existing_contract else self.existing_contract_sale_order_id.contract_end_date
                if contract_start_date and contract_end_date:
                    rec._generate_package_months(start_date=contract_start_date, end_date=contract_end_date)
        return res

    def _update_order_name(self, contract_prefix):
        """Ensures contract prefix is included in the order name correctly."""
        if contract_prefix not in self.name:
            name_parts = self.name.split('-')
            if len(name_parts) > 1:
                first_part = name_parts[:-1]
                last_part = name_parts[-1]
                if first_part and last_part:
                    self.name = f"{'-'.join(first_part)}-{contract_prefix}-{last_part}"
            
    def _get_contract_prefix(self, contract_type, project_number):
        """Returns the appropriate prefix for a contract type."""
        if self.opportunity_id:
            return project_number
        else:
            prefix_mapping = {
                'service': 'MC',
                'installation': 'IC',
                'supply': 'SC',
                'spare_parts': 'SP',
                'turnkey': 'TC',
                'spo': 'SPO',
            }
            return f"{prefix_mapping.get(contract_type, '')}-{project_number}"

    def _generate_package_months(self, start_date, end_date):
        """Generates package months for each annex in the order."""
        annexes = self._get_annexes_with_related_order()
        
        for annex in annexes:
            annex.tta_package_month_ids.unlink()  # Clear existing months
        
            current_date = start_date
            while current_date <= end_date:
                annex.tta_package_month_ids = [(0, 0, {
                    'month': current_date,
                    'package_id': False,
                })]
                # Move to the first day of the next month
                current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            invoice_vals['sale_project_number'] = self.project_number if not self.is_existing_contract else self.existing_contract_sale_order_id.project_number
            invoice_vals['sale_contract_type'] = self.contract_type
        return invoice_vals

    def generate_and_attach_contract(self):
        """Generates a contract PDF, attaches it to the sale order."""
        self.ensure_one()
        
        # Generate the contract PDF
        report_name = 'custom_addons.contract_template_raw'
        pdf_content, content_type = self.env['ir.actions.report']._render_qweb_pdf(report_name, [self.id])
        
        # Generate the attachment name
        contract_label = dict(self._fields['contract_type'].selection).get(self.contract_type) or ''
        attachment_name = self._get_print_report_name(f"{contract_label} Contract #{self.contract_number or ''}").replace(' ', '_').replace('/', '_')
        
        # Attach to the current record
        attachment = self.env['ir.attachment'].create({
            'name': attachment_name,
            'type': 'binary',
            'raw': pdf_content,
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        
        # Log message in chatter
        self.message_post(
            body = _("%s Contract #%s has been generated and attached. You can download it from here.") % (contract_label, self.contract_number or ''),
            attachment_ids = [attachment.id]
        )
    