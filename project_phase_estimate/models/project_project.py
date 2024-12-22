import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"

    estimate_ids = fields.One2many("project.estimate", "project_id")
