# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectProject(models.Model):
    _inherit = "project.project"

    def action_open_project_updates(self):
        self.ensure_one()
        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "res_model": "project.update",
            "view_mode": "tree,form",
            "domain": [("project_id", "=", self.id)],
            "context": {"default_project_id": self.id},
        }
