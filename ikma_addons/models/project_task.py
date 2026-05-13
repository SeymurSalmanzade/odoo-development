# DEPENDED sale_project
from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    elevator_number = fields.Char(string='Lift Number')
    lift_product_id = fields.Many2one('product.template', string='Lift', readonly=True)
    equipment_number = fields.Char(string='Equipment Number', related='lift_product_id.default_code')

    def action_view_so(self):
        action_window = super(ProjectTask, self).action_view_so()
        if self.env.user.has_group('ikma_addons.group_ikma_azerbaijan_user'):
            action_window['context'].update({
                'create': True,
            })
        return action_window