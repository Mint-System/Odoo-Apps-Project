import logging
from odoo import fields, models, api, _
_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = 'project.task'
    
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')
    estimate_id = fields.Many2one('project.estimate', string='Project Estimate', compute='_compute_estimate_id')
    progress = fields.Float(related='estimate_id.progress')

    @api.depends('phase_id')
    def _compute_estimate_id(self):
        for task in self:
            estimate_id = self.env['project.estimate'].search([
                ('phase_id', '=', task.phase_id.id),
                ('project_id', '=', task.project_id.id)
            ])[:1]
            
            task.estimate_id = estimate_id if estimate_id else 0.0
