from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import logging
from markupsafe import Markup

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    sale_purchase_count = fields.Integer(
        compute="_compute_sale_purchase_count")
    allow_worksheet_task_automation = fields.Boolean(default=False)
    project_worksheet_lines = fields.One2many(
        'project.worksheet.line', 'project_id', string='Worksheet Orders')

    @api.constrains('allow_worksheet_task_automation')
    def _check_project_worksheet_lines_length(self):
        for rec in self:
            if rec.allow_worksheet_task_automation and len(rec.project_worksheet_lines) == 0:
                raise UserError(
                    _("To enable worksheet task automation, at least one project worksheet line must be defined for the project."))

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if 'sale_line_id' in val and val['sale_line_id']:
                sale_order = self.env['sale.order.line'].browse(
                    val['sale_line_id']).order_id
                if sale_order.signed_contract and sale_order.project_number:
                    val['name'] = sale_order.project_number
        return super(Project, self).create(vals)

    @api.depends('sale_order_id')
    def _compute_sale_purchase_count(self):
        for rec in self:
            if rec.sale_order_id:
                rec.sale_purchase_count = self.env['purchase.order'].search_count(
                    [('sale_order_id', '=', rec.sale_order_id.id)])
            else:
                rec.sale_purchase_count = 0

    def action_view_so_purchases(self):
        self.ensure_one()
        sale_order_id = self.sale_order_id.id
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Purchases',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', sale_order_id if sale_order_id else '')],
            'context': {'default_sale_order_id': sale_order_id}
        }
        return action
    
    def _cron_create_tasks(self):
        automation_allowed_projects = self.search([('allow_worksheet_task_automation', '=', True)])
        
        if not automation_allowed_projects:
            _logger.info("Skipping creating tasks: No projects found with worksheet task automation enabled")
            return

        today = fields.Date.today()

        for project in automation_allowed_projects:
            project_worksheet_line = project.project_worksheet_lines.filtered(
                lambda l: l.planned_next and l.planned_at == today)[:1]

            if not project_worksheet_line:
                _logger.info(
                    f"Skipping creating task: No planned worksheets (project.worksheet.line) for the project [{project.name}] today")
                continue
            
            so_lines = self.env['sale.order.line'].search([
                ('project_id', '=', project.id),
                ('product_template_id.is_lift_service', '=', True),
                ('state', '=', 'sale')
            ])
            
            if not so_lines:
                _logger.info(
                    f"Skipping creating task: No sale order lines to create tasks for the project [{project.name}]")
                continue

            for line in so_lines:
                _logger.info(
                    f"Creating task for sale order line {line.id} - project {project.name}")

                created_task = self.env['project.task'].create({
                    "name": f"{line.lift_number} - {line.order_id.client_order_ref}",
                    "project_id": project.id,
                    "lift_product_id": line.product_template_id.id,
                    "worksheet_template_id": project_worksheet_line.worksheet_id.id,
                    "elevator_number": line.lift_number,
                })
                
                message = f"<b>EN:</b> Task <b>'{created_task.name}'</b> created for sale order line <b>'{line.name}'</b>"

                project.message_post(body=Markup(message))

            # Update worksheet order (project.worksheet.line) of the current project:
            # set current planned worksheet as not planned, and set the next worksheet as planned for the next month
            next_project_worksheet_line = project.project_worksheet_lines.filtered(
                lambda l: l.sequence > project_worksheet_line.sequence)[:1]

            project_worksheet_line.write({'planned_next': False})
            if next_project_worksheet_line:
                next_project_worksheet_line.write(
                    {'planned_next': True, 'planned_at': today + relativedelta(months=1)})
            else:
                # if current planned worksheet is the last one or there is only one worksheet, set the first one as planned next for the next month
                project.project_worksheet_lines[:1].write(
                    {'planned_next': True, 'planned_at': today + relativedelta(months=1)})
