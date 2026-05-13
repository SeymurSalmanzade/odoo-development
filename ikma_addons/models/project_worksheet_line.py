from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectWorksheetLine(models.Model):
    _name = 'project.worksheet.line'
    _description = 'Worksheet Line'

    project_id = fields.Many2one('project.project', string='Project')
    worksheet_id = fields.Many2one('worksheet.template', string="Worksheet")
    planned_at = fields.Date()
    planned_next = fields.Boolean(default=False)
    sequence = fields.Integer()

    @api.constrains('planned_next')
    def _check_planned_next(self):
        for line in self:
            if line.planned_next:
                existing = self.search([
                    ('project_id', '=', line.project_id.id),
                    ('planned_next', '=', True),
                    ('id', '!=', line.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Only one line can be marked as planned next for a project."))

                if not line.planned_at:
                    raise ValidationError(
                        _("Planned Date must be set when 'Planned Next' is enabled.")
                    )
