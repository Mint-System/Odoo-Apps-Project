from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    depend_on_ids_count = fields.Integer(
        string='Blocked By Count', compute='_compute_depend_on_ids_count'
    )

    def _compute_depend_on_ids_count(self):
        for task in self:
            task.depend_on_ids_count = len(task.depend_on_ids)

    def view_depend_on_ids(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Blocked By',
            'view_mode': 'kanban,form',
            'res_model': 'project.task',
            'domain': [('id', 'in', [t.id for t in self.depend_on_ids])],
        }
