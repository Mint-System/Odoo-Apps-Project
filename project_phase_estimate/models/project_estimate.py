import logging
from odoo import fields, models, api, _
from odoo.tools.float_utils import float_compare
_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _name = 'project.estimate'
    _description = 'Project Estimate'
    _rec_name = 'phase_id'
    _order = 'sequence'

    sequence = fields.Integer()
    project_id = fields.Many2one('project.project', string='Project')
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')
    task_ids = fields.Many2many('project.task', compute='_compute_task_ids', store=False)

    _sql_constraints = [
        ('project_phase_unique', 'unique(project_id, phase_id)', 'The combination of project and phase must be unique.'),
    ]

    @api.depends('project_id', 'phase_id', 'phase_id.task_ids')
    def _compute_task_ids(self):
        for estimate in self:
            estimate.task_ids = self.env['project.task'].search([
                ('phase_id', '=', estimate.phase_id.id),
                ('project_id', '=', estimate.project_id.id),
            ])

    planned_date_begin = fields.Datetime('Start date')
    planned_date_end = fields.Datetime('End date')

    planned_hours = fields.Float()
    effective_hours = fields.Float(compute='_compute_effective_hours', compute_sudo=True, store=False)
    remaining_hours = fields.Float(compute='_compute_remaining_hours', store=False)
    progress = fields.Float(compute='_compute_progress_hours', store=False)

    @api.depends('task_ids')
    def _compute_effective_hours(self):
        for estimate in self:
            estimate.effective_hours = sum(estimate.task_ids.timesheet_ids.mapped('unit_amount'))

    @api.depends('effective_hours', 'planned_hours')
    def _compute_remaining_hours(self):
        for estimate in self:
            estimate.remaining_hours = estimate.planned_hours - estimate.effective_hours

    @api.depends('effective_hours', 'planned_hours')
    def _compute_progress_hours(self):
        for estimate in self:
            if (estimate.planned_hours > 0.0):
                if float_compare(estimate.effective_hours, estimate.planned_hours, precision_digits=2) >= 0:
                    estimate.progress = 100
                else:
                    estimate.progress = round(100.0 * estimate.effective_hours / estimate.planned_hours, 2)
            else:
                estimate.progress = 0.0
