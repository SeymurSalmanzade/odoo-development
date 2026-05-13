from odoo import models, fields
from .sale_order import SALE_CONTRACT_TYPE

DEFAULT_CONTRACT_HTML = """
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Müqavilə</title>
        <style>
            body {
            font-family: 'Times New Roman'
            }
            p, ul {
                margin: 4px 0px;
            }
        </style>
    </head>
    <body>
        <div name="header" style="text-align: center;">
            <h5>
                <b>MÜQAVİLƏ № <span t-field="doc.contract_number"/></b>
            </h5>
        </div>
    </body>
</html>
"""

class SaleContractTemplate(models.Model):
    _name = "sale.contract.template"
    _description = "Sale Contract Template"
    
    name = fields.Char(string="Template Name", required=True)
    type = fields.Selection(selection=[
        *SALE_CONTRACT_TYPE.items()], string="Contract Type", required=True)
    arch = fields.Text(string="Template", required=True, default=DEFAULT_CONTRACT_HTML)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
