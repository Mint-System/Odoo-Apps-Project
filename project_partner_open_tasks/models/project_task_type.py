from odoo import api, fields, models, _, tools


class ProjectType(models.Model):
    _inherit = 'project.task.type'

    # is_done = fields.Boolean()
