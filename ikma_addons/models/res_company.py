from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    company_name_short = fields.Char(string="Company Name Short", store=True)
    sale_line_sequence_product_only = fields.Boolean(
        string="Order line number only for product",
        help="Check this to set Order line number only for product in Sale Order", default=True)
    spo_note = fields.Html(string="SPO Note", help="Additional note for SPO (Commercial Offer)", translate=True)
    annex_note_header = fields.Html(string="Annex Note Header", translate=True)
    annex_note_footer = fields.Html(string="Annex Note Footer", translate=True)
    service_invoice_note = fields.Html(string="Service Invoice Note", translate=True)
    
    # Additional fields
    director = fields.Char('Director')
    director_sign = fields.Binary("Director's Sign")
    stamp = fields.Binary('Stamp')
