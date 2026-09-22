from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    task_id = fields.Many2one(
        "project.task",
        string="Task",
        help="The project task linked to this ticket.",
    )

    @api.depends(
        "task_id",
        "task_id.sale_line_id",
        "partner_id",
        "use_helpdesk_sale_timesheet",
        "project_id.pricing_type",
        "project_id.sale_line_id",
    )
    def _compute_sale_line_id(self):
        tickets_with_task = self.filtered("task_id")
        for ticket in tickets_with_task:
            ticket.sale_line_id = ticket.task_id.sale_line_id
        return super(HelpdeskTicket, self - tickets_with_task)._compute_sale_line_id()
