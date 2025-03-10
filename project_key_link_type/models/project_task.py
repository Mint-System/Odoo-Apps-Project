import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    code = fields.Char(related="project_id.code")
