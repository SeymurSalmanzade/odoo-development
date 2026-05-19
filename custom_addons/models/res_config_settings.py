from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_line_sequence_product_only = fields.Boolean(related='company_id.sale_line_sequence_product_only', readonly=False)
    spo_note = fields.Html(related="company_id.spo_note", readonly=False)
    annex_note_header = fields.Html(related="company_id.annex_note_header", readonly=False)
    annex_note_footer = fields.Html(related="company_id.annex_note_footer", readonly=False)
    service_invoice_note = fields.Html(related="company_id.service_invoice_note", readonly=False)
