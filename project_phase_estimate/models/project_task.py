import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", string="Project Phase")
    estimate_id = fields.Many2one("project.estimate", string="Project Estimate", compute="_compute_estimate_id")
    estimate_progress = fields.Float(related="estimate_id.progress", string="Estimate Progress")

    @api.depends("phase_id")
    def _compute_estimate_id(self):
        for task in self:
            if task.phase_id and task.project_id:
                estimate_id = self.env["project.estimate"].search(
                    [
                        ("phase_id", "=", task.phase_id.id),
                        ("project_id", "=", task.project_id.id),
                    ]
                )[:1]

                if not estimate_id:
                    estimate_id = self.env["project.estimate"].create(
                        {
                            "project_id": task.project_id.id,
                            "phase_id": task.phase_id.id,
                            "planned_hours": 0.0,
                        }
                    )

                task.estimate_id = estimate_id
            else:
                task.estimate_id = False
