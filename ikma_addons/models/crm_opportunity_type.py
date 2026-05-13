from odoo import models, fields
from .sale_order import SALE_CONTRACT_TYPE

class CRMOpportunityType(models.Model):
    _name = 'crm.opportunity.type'
    _description = 'CRM Opportunity Type'
    
    name = fields.Char(string="Name")
    prefix = fields.Char(string="Prefix", help="Prefix for the sequence number of opporunities in this type.")
    contract_type = fields.Selection(selection=[
        *SALE_CONTRACT_TYPE.items()], string="Contract Type", help="Type of contract associated with this opportunity type.")
    