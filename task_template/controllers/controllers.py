# -*- coding: utf-8 -*-
# from odoo import http


# class TaskTemplate(http.Controller):
#     @http.route('/task_template/task_template', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_template/task_template/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_template.listing', {
#             'root': '/task_template/task_template',
#             'objects': http.request.env['task_template.task_template'].search([]),
#         })

#     @http.route('/task_template/task_template/objects/<model("task_template.task_template"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_template.object', {
#             'object': obj
#         })

