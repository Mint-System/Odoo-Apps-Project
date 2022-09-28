from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    code = fields.Char(
        string='Project Code',
        required=True,
        default='/',
        copy=False,
    )

    _sql_constraints = [
        ('project_project_unique_code', 'UNIQUE (code)', _('The code must be unique!')),
    ]

    def name_get(self):
        """Set proejct display name."""
        res = []
        for record in self:
            res.append((record.id, '[%s] %s' % (record.code, record.name)))
        return res

    def _set_code(self, vals):
        """Create project sequence from type."""
        type_id = self.type_id or self.env['project.type'].browse(vals.get('type_id'))
        if type_id:
            vals['code'] = type_id.sequence_id.next_by_id()
        return vals

    def write(self, vals):
        # Generate code if default is set.
        if self.code == '/':
            self._set_code(vals)    
        res = super(Project, self).write(vals)
        # Update analytic account
        self._update_analytic_account()
        return res

    @api.model
    def create(self, vals):
        # Generate code if default is set.
        if vals.get('code', '/') == '/':
            self._set_code(vals)
        # Setup andupdate analytic account
        analytic_account = self._create_analytic_account_from_values(vals)
        vals['analytic_account_id'] = analytic_account.id
        res = super().create(vals)
        res._update_analytic_account()
        return res
    
    def _update_analytic_account(self):
        if self.analytic_account_id:
            self.analytic_account_id.write({
                'name': '[%s] %s' % (self.code, self.name),
                'partner_id': self.partner_id.id
            })