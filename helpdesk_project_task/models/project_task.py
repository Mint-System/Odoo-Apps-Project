from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    helpdesk_ticket_ids = fields.Many2many(
        "helpdesk.ticket",
        string="Tickets",
        relation="helpdesk_ticket_project_task_rel",
        column1="task_id",
        column2="ticket_id",
    )
    helpdesk_ticket_count = fields.Integer(string="Ticket Count", compute="_compute_helpdesk_ticket_count")

    @api.depends("helpdesk_ticket_ids")
    def _compute_helpdesk_ticket_count(self):
        for task in self:
            task.helpdesk_ticket_count = len(task.helpdesk_ticket_ids)

    def action_view_helpdesk_tickets(self):
        self.ensure_one()
        if len(self.helpdesk_ticket_ids) == 1:
            action = {
                "type": "ir.actions.act_window",
                "res_model": "helpdesk.ticket",
                "view_mode": "form",
                "res_id": self.helpdesk_ticket_ids.id,
                "target": "current",
            }
        else:
            action = {
                "type": "ir.actions.act_window",
                "res_model": "helpdesk.ticket",
                "view_mode": "tree,form",
                "domain": [("id", "in", self.helpdesk_ticket_ids.ids)],
                "target": "current",
            }
        return action
