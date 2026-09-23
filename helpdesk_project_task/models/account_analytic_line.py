from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.depends("helpdesk_ticket_id")
    def _compute_task_id(self):
        timesheets_with_matching_task = self.filtered(
            lambda line: line.task_id
            and line.helpdesk_ticket_id
            and line.helpdesk_ticket_id.task_id == line.task_id
        )
        super(AccountAnalyticLine, self - timesheets_with_matching_task)._compute_task_id()

    @api.depends("task_id", "project_id")
    def _compute_helpdesk_ticket_id(self):
        timesheets_with_matching_task = self.filtered(
            lambda line: line.task_id
            and line.helpdesk_ticket_id
            and line.helpdesk_ticket_id.task_id == line.task_id
        )
        super(AccountAnalyticLine, self - timesheets_with_matching_task)._compute_helpdesk_ticket_id()

    @api.constrains("task_id", "helpdesk_ticket_id")
    def _check_no_link_task_and_ticket(self):
        invalid = self.filtered(
            lambda line: line.task_id
            and line.helpdesk_ticket_id
            and line.helpdesk_ticket_id.task_id != line.task_id
        )
        if invalid:
            raise ValidationError(_(
                "You cannot link a timesheet entry to a task and a ticket at the same time."
            ))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("helpdesk_ticket_id") and not vals.get("task_id"):
                ticket = self.env["helpdesk.ticket"].sudo().browse(vals["helpdesk_ticket_id"])
                if ticket.task_id:
                    vals["task_id"] = ticket.task_id.id
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("helpdesk_ticket_id") and "task_id" not in vals:
            ticket = self.env["helpdesk.ticket"].sudo().browse(vals["helpdesk_ticket_id"])
            if ticket.task_id:
                vals["task_id"] = ticket.task_id.id
        return super().write(vals)
