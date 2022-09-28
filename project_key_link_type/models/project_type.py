
from odoo import _, api, fields, models


class ProjectType(models.Model):
    _inherit = 'project.type'
    
    sequence_id = fields.Many2one('ir.sequence')