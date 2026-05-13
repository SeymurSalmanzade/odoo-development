from odoo import fields, api, models
from .sale_order import SALE_CONTRACT_TYPE

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'ikma.common']
    
    text_amount = fields.Char(string="Total in Words", compute="_compute_amount_total")
    sale_project_number = fields.Char(string="Project Number", help="Project number of the Sale Order")
    sale_contract_type = fields.Selection(selection=[
        *SALE_CONTRACT_TYPE.items()], string="Contract Type")
    service_invoice_month_count = fields.Integer(string="Service Invoice Month Count", default=1)
    service_invoice_description = fields.Char(string="Service Invoice Description", translate=True, default="Liftlərə aylıq texniki xidmət")
    service_invoice_note = fields.Html(string="Service Invoice Note", default=lambda self: self.env.company.with_context(lang=self.env.user.lang).service_invoice_note)
    
    @api.depends('amount_total')
    def _compute_amount_total(self):
        for move in self:
            move.text_amount = move._amount_to_word_az(move.amount_total)
