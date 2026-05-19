# -*- coding: utf-8 -*-

from odoo import models, fields

class TTAPackages(models.Model):
    _name = 'tta.packages'
    _description = 'TTA Packages'

    name = fields.Char(string="Name")
    note_az = fields.Html(string="Note AZ")
    note_en = fields.Html(string="Note EN")
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    