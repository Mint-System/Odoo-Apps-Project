# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class PrepareProjectUpdateWizard(models.TransientModel):
    _name = "prepare.project.update.wizard"
    _description = "Prepare Project Update Wizard"

    batch = fields.Char(required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "batch" in fields_list:
            today = fields.Date.context_today(self)
            year = today.strftime("%Y")
            week = today.isocalendar()[1]
            res["batch"] = f"{year}-W{week:02d}"
        return res

    def action_prepare(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            return {"type": "ir.actions.act_window_close"}

        projects = self.env["project.project"].browse(active_ids)
        for project in projects:
            status = "on_track"
            if project.last_update_status and project.last_update_status != "to_define":
                status = project.last_update_status
            self.env["project.update"].create(
                {
                    "project_id": project.id,
                    "batch": self.batch,
                    "name": "Project Status",
                    "description": False,
                    "status": status,
                }
            )

        return {
            "name": _("Project Updates"),
            "type": "ir.actions.act_window",
            "res_model": "project.update",
            "view_mode": "tree,form",
            "target": "current",
            "domain": [("batch", "=", self.batch)],
            "context": {
                "search_default_group_by_batch": 1,
                "expand": True,
            },
        }
