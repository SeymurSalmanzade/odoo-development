from odoo import models

class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'
    
    def action_lost_reason_apply(self):
        for lead in self.lead_ids:
            lead.lost_feedback = self.lost_feedback
        return super().action_lost_reason_apply()
            