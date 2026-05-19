from odoo import models, fields
from .sale_order import SALE_CONTRACT_TYPE, SALE_SERVICE_ADDENDUM_TYPE, SALE_INSTALLATION_ADDENDUM_TYPE

DEFAULT_ADDENDUM_HTML = """
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Addendum</title>
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
                <b>Addendum (<span t-if="doc.contract_type == 'service'" t-field="doc.service_addendum"/>
                            <span t-elif="doc.contract_type == 'installation'" t-field="doc.installation_addendum"/>)
                </b>
            </h5>
        </div>
    </body>
</html>
"""

class SaleAddendumTemplate(models.Model):
    _name = "sale.addendum.template"
    _description = "Sale Addendum Template"
    
    name = fields.Char(string="Template Name", required=True)
    contract_type = fields.Selection(selection=[
        *SALE_CONTRACT_TYPE.items()], string="Contract Type", required=True)
    type = fields.Selection(selection=[
        *SALE_SERVICE_ADDENDUM_TYPE.items(),
        *SALE_INSTALLATION_ADDENDUM_TYPE.items()], string="Addendum Type", required=True)
    arch = fields.Text(string="Template", required=True, default=DEFAULT_ADDENDUM_HTML)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    