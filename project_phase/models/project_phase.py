import logging
from odoo import fields, models, api, _
_logger = logging.getLogger(__name__)


class ProjectPhase(models.Model):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'sequence'
    
    active = fields.Boolean(default=True)
    name = fields.Char(string='Phase Name')
    sequence = fields.Integer()
    project_id = fields.Many2one('project.project', string='Project', default=lambda self: self.env.context.get('default_project_id'))
    start_date = fields.Date(copy=False)
    end_date = fields.Date(copy=False)
    company_id = fields.Many2one('res.company',string='Company', default=lambda self: self.env['res.company']._company_default_get())
    user_id = fields.Many2one('res.users', string='Assignees', default=lambda self: self.env.uid)
    task_ids = fields.One2many('project.task', 'phase_id')
    task_count = fields.Integer(compute='_compute_get_task', string='Count')
    notes = fields.Text()

    _sql_constraints = [
        ('name_project_id_unique', 'unique(name, project_id)', 'The combination of name and project must be unique.'),
    ]

    def action_project_phase_task(self):
        self.ensure_one()
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('phase_id', '=', self.id)],
        }

    @api.depends('task_ids')
    def _compute_get_task(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)
