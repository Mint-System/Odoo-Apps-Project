import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    phase_id = fields.Many2one("project.task.phase", related="task_id.phase_id")
