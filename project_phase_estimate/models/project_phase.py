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
    estimate_count = fields.Integer(compute="_compute_get_estimate", string="Estimate Count")

    @api.depends("estimate_ids.project_id")
    def _compute_project_ids(self):
        for phase in self:
            phase.project_ids = phase.estimate_ids.project_id

    def action_project_estimate(self):
        self.ensure_one()
        return {
            "name": "Project Estimates",
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "project.estimate",
            "domain": [("phase_id", "=", self.id)],
            "context": {"default_project_id": self.env.context.get("default_project_id")},
        }

    @api.depends("estimate_ids")
    def _compute_get_estimate(self):
        for rec in self:
            rec.estimate_count = len(rec.estimate_ids)
