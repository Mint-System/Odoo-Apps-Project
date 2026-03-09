import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"

    allow_estimate = fields.Boolean(default=True, help="Add estimates linked to phases to this project.")
    estimate_ids = fields.One2many("project.estimate", "project_id")

    def action_view_estimates(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Estimates",
            "res_model": "project.estimate",
            "view_mode": "tree,form",
            "context": {"default_project_id": self.id, "search_default_project_id": self.id},
        }
