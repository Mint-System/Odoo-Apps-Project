import logging

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _name = "project.estimate"
    _description = "Project Estimate"
    _rec_name = "phase_id"
    _order = "sequence"

    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    project_id = fields.Many2one("project.project")
    phase_id = fields.Many2one("project.task.phase", string="Project Phase")

    start_date = fields.Date(copy=False)
    end_date = fields.Date(copy=False)

    planned_hours = fields.Float()
    effective_hours = fields.Float(compute="_compute_effective_hours", compute_sudo=True, store=True)
    remaining_hours = fields.Float(compute="_compute_remaining_hours", store=True)
    progress = fields.Float(compute="_compute_progress_hours", store=True, group_operator="avg")

    @api.depends("project_id", "phase_id", "phase_id.task_ids", "start_date", "end_date")
    def _compute_effective_hours(self):
        for estimate in self:
            task_ids = (
                self.with_context(active_test=False)
                .env["project.task"]
                .search(
                    [
                        ("phase_id", "=", estimate.phase_id.id),
                        ("project_id", "=", estimate.project_id.id),
                    ]
                )
            )
            effective_hours = task_ids.timesheet_ids

            if self.env.context.get("validated_hours_only", False):
                effective_hours = effective_hours.filtered(lambda line: line.validated)

            if estimate.start_date:
                effective_hours = effective_hours.filtered(lambda line: line.date >= estimate.start_date)

            if estimate.end_date:
                effective_hours = effective_hours.filtered(lambda line: line.date <= estimate.end_date)

            estimate.effective_hours = sum(effective_hours.mapped("unit_amount"))

    @api.depends("planned_hours", "effective_hours")
    def _compute_remaining_hours(self):
        for estimate in self:
            estimate.remaining_hours = estimate.planned_hours - estimate.effective_hours

    @api.depends("remaining_hours")
    def _compute_progress_hours(self):
        """
        Compare effective hours with planned hours.
        If planned hours is zero then set progress to 100%.
        When effective hours exceeds planned hours set progress to 100%.
        """
        for estimate in self:
            if estimate.planned_hours > 0.0:
                if (
                    float_compare(
                        estimate.effective_hours,
                        estimate.planned_hours,
                        precision_digits=2,
                    )
                    >= 0
                ):
                    estimate.progress = 100
                else:
                    estimate.progress = round(100.0 * estimate.effective_hours / estimate.planned_hours, 2)
            else:
                estimate.progress = 100
