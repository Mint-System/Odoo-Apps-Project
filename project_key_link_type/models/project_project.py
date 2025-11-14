import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)
from odoo.osv.expression import AND, OR


class Project(models.Model):
    _inherit = "project.project"

    type_id = fields.Many2one(copy=True)
    key = fields.Char(
        string="Project Key",
        required=True,
        default="/",
        copy=False,
    )

    def name_get(self):
        """Set proejct display name."""
        res = []
        for record in self:
            res.append((record.id, "[%s] %s" % (record.key, record.name)))
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = OR([[("name", "ilike", name)], [("key", "ilike", name)]])
        records = self.search(AND([args, domain]), limit=limit)
        return records.name_get()

    def _set_key(self, vals):
        """
        Create project sequence from type.
        """
        type_id = self.type_id or self.env["project.type"].browse(vals.get("type_id"))
        if type_id:
            vals["key"] = type_id.sequence_id.next_by_id()
        return vals

    def write(self, vals):
        """
        Generate key if default is set.
        """
        if ((vals.get("key") or self.key) == "/") and not self.is_template:
            self._set_key(vals)
        res = super().write(vals)
        # Update analytic account
        self._update_analytic_account()
        return res

    @api.model
    def create(self, vals):
        """
        Generate key if default is set.
        """
        if vals.get("key", "/") == "/":
            self._set_key(vals)
        # Setup and update analytic account
        analytic_account = self._create_analytic_account_from_values(vals)
        vals["analytic_account_id"] = analytic_account.id
        res = super().create(vals)
        res._update_analytic_account()
        return res

    def _update_analytic_account(self):
        for project in self.filtered(lambda p: p.analytic_account_id):
            project.analytic_account_id.write(
                {
                    "name": "[%s] %s" % (project.key, project.name),
                    "partner_id": project.partner_id.id,
                }
            )
