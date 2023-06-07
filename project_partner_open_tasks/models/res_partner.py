from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    task_open_count = fields.Integer(compute='_compute_task_open_count', string='# Open Tasks')

    def _compute_task_open_count(self):
        # Retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        task_data = self.env['project.task']._read_group(
            domain=[('partner_id', 'in', all_partners.ids),('is_closed', '=', False)],
            fields=['partner_id'], groupby=['partner_id']
        )

        self.task_open_count = 0
        for group in task_data:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.task_open_count += group['partner_id_count']
                partner = partner.parent_id
    