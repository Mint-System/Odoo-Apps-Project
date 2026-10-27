# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class ProjectUpdate(models.Model):
    _inherit = "project.update"
    _order = "batch, project_user_id, date desc"

    batch = fields.Char()
    partner_id = fields.Many2one("res.partner", related="project_id.partner_id", store=True, readonly=True)
    project_user_id = fields.Many2one("res.users", related="project_id.user_id", store=True, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("batch") and not vals.get("name"):
                vals["name"] = "Project Status"
        return super().create(vals_list)

    def action_open_form(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.name,
            "res_model": "project.update",
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }

    def action_view_project_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.project_id.name,
            "res_model": "project.task",
            "view_mode": "kanban,tree,form",
            "domain": [("project_id", "=", self.project_id.id)],
            "context": {"default_project_id": self.project_id.id},
        }
