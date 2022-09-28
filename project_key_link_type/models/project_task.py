from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    code = fields.Char(related='project_id.code')
    # code = fields.Char(
    #     string='Task Code',
    #     required=True,
    #     default='/',
    #     copy=False,
    # )

    # _sql_constraints = [
    #     ('project_task_unique_code', 'UNIQUE (code)', _('The code must be unique!')),
    # ]

    # def name_get(self):
    #     """Set task display name."""
    #     res = []
    #     for record in self:
    #         res.append((record.id, '[%s] %s' % (record.code, record.name)))
    #     return res