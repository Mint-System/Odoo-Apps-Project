# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectCollaborator(models.Model):
    _inherit = "project.collaborator"

    partner_id = fields.Many2one(readonly=False)
