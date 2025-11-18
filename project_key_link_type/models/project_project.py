import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    type_id = fields.Many2one(copy=True, inverse="_inverse_type_id")

    def _inverse_type_id(self):
        """
        Create project sequence from type.
        """
        for project in self:
            if project.type_id and not project.is_template:
                project.key = project.type_id.sequence_id.next_by_id()

    @api.onchange("name")
    def _onchange_project_name(self):
        """
        Disable this onchange method.
        """
        return False
