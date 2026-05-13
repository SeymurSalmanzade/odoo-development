from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'
    
    opportunity_type_id = fields.Many2one('crm.opportunity.type', string="Opportunity Type")
    
    def _action_merge(self):
        result_opportunity = super()._action_merge()
        if result_opportunity and self.env.user.has_group('ikma_addons.group_ikma_azerbaijan_user'):
            result_opportunity.opportunity_type_id = self.opportunity_type_id
        return result_opportunity

    def _action_convert(self):
        if not self.env.user.has_group('ikma_addons.group_ikma_azerbaijan_user'):
            return super()._action_convert()
        result_opportunities = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        res = super()._action_convert()
        for opp in result_opportunities.sorted(key=lambda x: x.id):
            opp.opportunity_type_id = self.opportunity_type_id
        return res
    