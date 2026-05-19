from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    def _get_default_opportunity_no(self):
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            return _('New')
        return False
    
    opportunity_no = fields.Char(string="Number", required=True, copy=False, index='trigram', default=_get_default_opportunity_no)
    opportunity_type_id = fields.Many2one('crm.opportunity.type', string="Opportunity Type")
    lost_feedback = fields.Html(string="Closing Note", copy=False)
    project_location = fields.Char(string="Project Location")
    equipment_type_ids = fields.Many2many("crm.equipment.type", string="Equipment Type")
    equipment_qty = fields.Integer(string="Equipment Quantity", default=1)
    sales_account_name = fields.Char(string="Sales Account Name")
    
    def _assign_opportunity_number(self, opportunity_type=None, seq_date=None):
        """Assign a unique number to the opportunity, using the type prefix and sequence."""
        self.ensure_one()
        opportunity_type = opportunity_type or self.opportunity_type_id
        if not opportunity_type or not opportunity_type.prefix:
            raise UserError(_("Please select an Opportunity Type with a prefix before creating or converting an opportunity."))
        if self.opportunity_no == _('New'):
            raw_sequence = self.env['ir.sequence'].with_company(self.env.company).next_by_code(
                'crm.lead.opp.number', sequence_date=seq_date
            ) or None
            if raw_sequence:
                raw_sequence_parts = raw_sequence.split('-')
                if len(raw_sequence_parts) > 1:
                    first_part = raw_sequence_parts[:-1]
                    last_part = raw_sequence_parts[-1]
                    if first_part and last_part:
                        self.opportunity_no = f"{'-'.join(first_part)}-{opportunity_type.prefix}-{last_part}"

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            for lead in leads:
                # Only apply to opportunity with "New" number
                if lead.type == 'opportunity' and lead.opportunity_no == _('New') and lead.opportunity_type_id:
                    seq_date = lead.date_open or fields.Datetime.now()
                    lead._assign_opportunity_number(
                        opportunity_type=lead.opportunity_type_id,
                        seq_date=fields.Datetime.context_timestamp(lead, fields.Datetime.to_datetime(seq_date)),
                    )
        return leads

    def write(self, vals):
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            if 'opportunity_type_id' in vals:
                for lead in self.sorted(key=lambda x: x.id):
                    if lead.type == 'opportunity' and lead.opportunity_no == _('New'):
                        seq_date = vals.get('date_open', lead.date_open) or fields.Datetime.now()
                        opportunity_type = self.env['crm.opportunity.type'].browse(vals['opportunity_type_id'])
                        lead._assign_opportunity_number(
                            opportunity_type=opportunity_type,
                            seq_date=fields.Datetime.context_timestamp(lead, fields.Datetime.to_datetime(seq_date)),
                        )
        return super().write(vals)
        
    def regenerate_opportunity_no_prefix(self):
        if self.env.user.has_group('custom_addons.group_custom_azerbaijan_user'):
            for rec in self:
                if not rec.opportunity_type_id:
                    raise UserError(_("Select an opportunity type first!"))
                if rec.opportunity_no == _('New'):
                    seq_date = rec.date_open or fields.Datetime.now()
                    rec._assign_opportunity_number(
                        opportunity_type=rec.opportunity_type_id,
                        seq_date=fields.Datetime.context_timestamp(rec, fields.Datetime.to_datetime(seq_date)),
                    )
                else:
                    splitted_no = rec.opportunity_no.split('-')
                    if len(splitted_no) > 2:
                        first_part = splitted_no[:-2]
                        last_part = splitted_no[-1]
                        if first_part and last_part:
                            rec.opportunity_no = f"{'-'.join(first_part)}-{rec.opportunity_type_id.prefix}-{last_part}"
                    