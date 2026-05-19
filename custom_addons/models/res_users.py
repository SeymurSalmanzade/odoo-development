from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self,vals):
        for val in vals:
            if val['sel_groups_1_10_11'] == 10:
                consumption_location_vals = {
                    "name": f"Consumption - {val['name']}",
                    "usage": "inventory",
                    "scrap_location": True
                }
                consumption_location_id = self.env['stock.location'].create(consumption_location_vals)
                val['consumption_location_id'] = consumption_location_id.id

                internal_location_vals = {
                    "name": f"Internal - {val['name']}",
                    "usage": "internal"
                }
                internal_location_id = self.env['stock.location'].create(internal_location_vals)
                val['internal_location_id'] = internal_location_id.id

        return super(ResUsers,self).create(vals)
