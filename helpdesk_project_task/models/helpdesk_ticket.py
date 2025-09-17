from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    project_task_ids = fields.Many2many(
        "project.task",
        string="Tasks",
        relation="helpdesk_ticket_project_task_rel",
        column1="ticket_id",
        column2="task_id",
    )
    project_task_count = fields.Integer(string="Task Count", compute="_compute_project_task_count")

    @api.depends("project_task_ids")
    def _compute_project_task_count(self):
        for ticket in self:
            ticket.project_task_count = len(ticket.project_task_ids)

    def action_view_project_tasks(self):
        self.ensure_one()
        if len(self.project_task_ids) == 1:
            action = {
                "type": "ir.actions.act_window",
                "res_model": "project.task",
                "view_mode": "form",
                "res_id": self.project_task_ids.id,
                "target": "current",
            }
        else:
            action = {
                "type": "ir.actions.act_window",
                "res_model": "project.task",
                "view_mode": "tree,form",
                "domain": [("id", "in", self.project_task_ids.ids)],
                "target": "current",
            }
        return action
