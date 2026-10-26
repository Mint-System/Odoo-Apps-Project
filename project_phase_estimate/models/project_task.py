import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", string="Project Phase")
    estimate_id = fields.Many2one("project.estimate", string="Project Estimate", compute="_compute_estimate_id")
    estimate_progress = fields.Float(related="estimate_id.progress", string="Estimate Progress")
    estimate_description = fields.Char(compute="_compute_estimate_description", string="Estimate Description")
    show_estimate = fields.Boolean(compute="_compute_show_estimate", string="Show Estimate")

    @api.depends("phase_id", "estimate_id.planned_hours")
    def _compute_show_estimate(self):
        for task in self:
            task.show_estimate = bool(task.phase_id and (task.estimate_id.planned_hours or 0.0) > 0)

    @api.depends("estimate_id.effective_hours", "estimate_id.planned_hours")
    def _compute_estimate_description(self):
        for task in self:
            effective = task.estimate_id.effective_hours or 0.0
            planned = task.estimate_id.planned_hours or 0.0
            task.estimate_description = "{} / {}".format(
                self._format_estimate_hours(effective),
                self._format_estimate_hours(planned),
            )

    def _format_estimate_hours(self, hours):
        self.ensure_one()
        total_minutes = int(round(max(hours, 0.0) * 60))
        hh = total_minutes // 60
        mm = total_minutes % 60
        return f"{hh:02d}:{mm:02d}"

    @api.depends("phase_id")
    def _compute_estimate_id(self):
        for task in self:
            if task.phase_id and task.project_id:
                estimate_id = self.env["project.estimate"].search(
                    [
                        ("phase_id", "=", task.phase_id.id),
                        ("project_id", "=", task.project_id.id),
                        ("is_in_progress", "=", True),
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("parent_id") and not vals.get("phase_id"):
                parent = self.browse(vals["parent_id"])
                vals["phase_id"] = parent.phase_id.id
        return super().create(vals_list)
