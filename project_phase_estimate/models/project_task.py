import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", string="Project Phase")
    estimate_id = fields.Many2one(
        "project.estimate", string="Project Estimate", compute="_compute_estimate_id", store=True
    )
    estimate_progress = fields.Float(related="estimate_id.progress", string="Estimate Progress")

    @api.depends("phase_id", "phase_id.project_id", "project_id")
    def _compute_estimate_id(self):
        for task in self:
            estimate = self.env["project.estimate"].search(
                [
                    ("phase_id", "=", task.phase_id.id),
                    ("project_id", "=", task.project_id.id),
                ],
                limit=1,
            )

            task.estimate_id = estimate.id if estimate else False
