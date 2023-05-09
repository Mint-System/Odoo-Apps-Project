from odoo import api, fields, models, _, tools


class ProjectPhase(models.Model):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'sequence'
    
    name = fields.Char(string='Phase Name')
    sequence = fields.Integer()
    project_id = fields.Many2one('project.project',string='Project',default=lambda self: self.env.context.get('default_project_id'))
    start_date = fields.Date(copy=False)
    end_date = fields.Date(copy=False)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env['res.company']._company_default_get())
    user_id = fields.Many2one('res.users', string='Assignees', default=lambda self: self.env.uid)
    task_count = fields.Integer(compute='_compute_get_task',string='Count')
    notes = fields.Text()

    def action_project_phase_task(self):
        self.ensure_one()
        return {
            'name': 'Tasks',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('phase_id', '=', self.id)],
        }

    def _compute_get_task(self):
        for rec in self:
            records = self.env['project.task'].search([('phase_id','=',rec.id)])
            rec.task_count = len(records)