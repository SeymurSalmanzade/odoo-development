from odoo import models, api
import ast

class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"
    
    @api.depends('composition_mode', 'model', 'res_domain', 'res_ids', 'template_id', 'template_id.merge_record_attachments')
    def _compute_attachment_ids(self):
        super()._compute_attachment_ids()
        for composer in self:
            # If the feature is enabled, and the composer is set to a single record
            if (composer.template_id and composer.template_id.merge_record_attachments and composer.model and composer.res_ids):
                try:
                    res_id_list = ast.literal_eval(composer.res_ids)
                except Exception:
                    res_id_list = []
                if res_id_list:
                    # Get attachments for the current record
                    record_attachments = self.env['ir.attachment'].search([
                        ('res_model', '=', composer.model),
                        ('res_id', '=', res_id_list)
                    ])
                    # Merge existing with record attachments (avoid duplicates)
                    composer.attachment_ids = [(4, attachment.id) for attachment in record_attachments]
