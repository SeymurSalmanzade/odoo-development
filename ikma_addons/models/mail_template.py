from odoo import models, fields

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    merge_record_attachments = fields.Boolean(string="Merge Record Attachments", default=False, help="If checked, attachments from the record will be merged into the email template attachments.")
    