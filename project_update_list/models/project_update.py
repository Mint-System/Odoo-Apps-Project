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

    collaborator_ids = fields.Many2many(
        "res.users",
        compute="_compute_collaborator_ids",
        string="Collaborators",
    )

    @api.depends("project_id.collaborator_ids", "project_id.collaborator_ids.partner_id")
    def _compute_collaborator_ids(self):
        projects = self.mapped("project_id")
        all_partner_ids = projects.collaborator_ids.partner_id.ids
        user_map = {}
        if all_partner_ids:
            for user in self.env["res.users"].search([("partner_id", "in", all_partner_ids)]):
                user_map[user.partner_id.id] = user.id
        for update in self:
            partner_ids = update.project_id.collaborator_ids.partner_id.ids
            update.collaborator_ids = [user_map[p] for p in partner_ids if p in user_map]

    def action_open_form(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.project_id.name,
            "res_model": "project.update",
            "view_mode": "tree,form",
            "domain": [("project_id", "=", self.project_id.id)],
            "context": {"default_project_id": self.project_id.id},
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
