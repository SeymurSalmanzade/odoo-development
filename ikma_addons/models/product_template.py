# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_lift_service = fields.Boolean(string='Is Lift Service?', default=False)
    lift_number = fields.Char(string="Number")
    lift_type = fields.Char(string="Type")
    lift_supply_line = fields.Char(string="Supply Line")
    lift_speed = fields.Float(string="Speed (m/s)")
    lift_load_capacity = fields.Float(string="Load Capacity (kg)")
    lift_floor_number = fields.Integer(string="Number of Floors",default=1)
    lift_stop_number = fields.Integer(string="Number of Stops",default=1)
    lift_passport_deadline = fields.Date(string="Passport Deadline")
    lift_warning_days = fields.Integer(string="Warning Days", default=7, help="Reminder days before deadline.")
    lift_attendee_ids = fields.Many2many('res.users', string='Attendees')
    
    @api.onchange('detailed_type')
    def _onchange_detailed_type(self):
        if self.detailed_type == 'service':
            self.uom_id = self.env.ref('uom.product_uom_unit').id
                            
    @api.model
    def _check_passport_deadline(self):
        """Check and trigger alarms for lift passport deadlines."""
        today = fields.Date.today()
        products = self._get_lift_service_products()

        for product in products:
            warning_days = product.lift_warning_days
            if self._should_trigger_warning(product, warning_days, today):
                self._handle_warning_notification(product)

    def _get_lift_service_products(self):
        """Retrieve all products that require lift passport service tracking."""
        return self.search([
            ('is_lift_service', '=', True),
            ('lift_passport_deadline', '!=', False)
        ])

    def _should_trigger_warning(self, product, warning_days, today):
        """Determine if an alarm should be triggered today."""
        delta = timedelta(**{'days': warning_days})
        reminder_date = product.lift_passport_deadline - delta
        return reminder_date == today

    def _handle_warning_notification(self, product):
        """Dispatch the alarm based on its type."""
        product_url = product._get_html_link()
        task_description = f"The passport deadline for <b>{product_url}</b> is approaching. Please take action."
        activity_note = task_description + '<br/>' + '<blockquote>If you done this task, please mark it as done for all attendees.</blockquote>'
        title = f"Passport Expiry Reminder for {product.display_name}"
        
        product_related_sale_orders = self.env['sale.report'].sudo().search([('product_tmpl_id', '=', product.id)]).mapped('order_reference')
        project_numbers = [order.project_number for order in product_related_sale_orders] if product_related_sale_orders else []

        if project_numbers:
            title = title + f" in Project(s): {', '.join(project_numbers)}"
        
        attendees = product.lift_attendee_ids
        self._create_todo_task_and_activity(attendees, title, task_description, activity_note, product.lift_passport_deadline)

    def _create_todo_task_and_activity(self, attendees, title, task_description, activity_note, deadline):
        """Create a to-do task for attendees and create an activity for the task."""
        deadline_datetime = deadline.strftime('%Y-%m-%d 19:59:59')
        task = self.env['project.task'].sudo().create({
            'name': title,
            'description': task_description,
            'user_ids': [(4, attendee.id) for attendee in attendees],
            'date_deadline': deadline_datetime,
        })
        for attendee in attendees:
            self.env['mail.activity'].sudo().create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': activity_note,
                'res_id': task.id,
                'res_model_id': self.env['ir.model']._get('project.task').id,
                'date_deadline': task.date_deadline,
                'user_id': attendee.id,
            })
