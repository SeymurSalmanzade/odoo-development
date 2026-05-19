from odoo import models, fields

class CRMEquipmentType(models.Model):
    _name = 'crm.equipment.type'
    _description = 'CRM Equipment Type'

    name = fields.Char(string="Equipment Type", required=True)
    