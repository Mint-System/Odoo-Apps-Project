import logging
from odoo import fields, models, api, _
_logger = logging.getLogger(__name__)


class ProjectPhase(models.Model):
    _inherit = 'project.task.phase'

    estimate_ids = fields.One2many('project.estimate', 'phase_id')
    estimate_count = fields.Integer(compute='_compute_get_estimate', string='Estimate Count')

    def action_project_estimate(self):
        self.ensure_one()
        return {
            'name': 'Project Estimates',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'project.estimate',
            'domain': [('phase_id', '=', self.id)],
        }

    @api.depends('estimate_ids')
    def _compute_get_estimate(self):
        for rec in self:
            rec.estimate_count = len(rec.estimate_ids)
