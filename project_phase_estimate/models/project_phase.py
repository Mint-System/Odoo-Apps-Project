import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProjectPhase(models.Model):
    _inherit = "project.task.phase"

    estimate_ids = fields.One2many("project.estimate", "phase_id")
    project_ids = fields.Many2many(
        "project.project",
        compute="_compute_project_ids",
        store=True,
        readonly=True,
    )
    estimate_count = fields.Integer(compute="_compute_estimate_count", string="Estimate Count", store=True)
    estimate_in_progress_count = fields.Integer(compute="_compute_estimate_count", string="Estimate Count", store=True)

    @api.depends("estimate_ids.project_id")
    def _compute_project_ids(self):
        for phase in self:
            phase.project_ids = phase.estimate_ids.project_id

    def action_project_estimate(self):
        self.ensure_one()
        default_project_id = self.env.context.get("default_project_id")
        context = {"default_project_id": default_project_id}
        if default_project_id:
            context["search_default_project_id"] = default_project_id
        return {
            "name": "Project Estimates",
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "project.estimate",
            "domain": [("phase_id", "=", self.id)],
            "context": context,
        }

    @api.depends("estimate_ids", "estimate_ids.is_in_progress")
    def _compute_estimate_count(self):
        for rec in self:
            rec.estimate_count = len(rec.estimate_ids)
            rec.estimate_in_progress_count = len(rec.estimate_ids.filtered("is_in_progress"))
