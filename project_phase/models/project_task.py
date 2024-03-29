from odoo import api, fields, models, _, tools


class Task(models.Model):
    _inherit = 'project.task'    
    
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')
    user_id = fields.Many2one('res.users', string='Assignee', default=lambda self: self.env.uid)
