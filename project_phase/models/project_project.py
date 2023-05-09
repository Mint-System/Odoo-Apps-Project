from odoo import api, fields, models, _, tools


class ProjectProject(models.Model):
    _inherit='project.project'
    
    project_phase_count = fields.Integer('Job Note', compute='_compute_get_project_phase_count')

    def _compute_get_project_phase_count(self):
        for project_phase in self:
            project_phase_ids = self.env['project.task.phase'].search([('project_id','=',project_phase.id)])
            project_phase.project_phase_count = len(project_phase_ids)

    def action_project_phase(self):
        self.ensure_one()
        return {
            'name': 'Phases',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.task.phase',
            'domain': [('project_id', '=', self.id)],
        }


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"
    
    phase_id = fields.Many2one('project.task.phase', string='Project Phase')
    
    
    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                   
                    t.date_end as date_end,
                    t.date_last_stage_update as date_last_stage_update,
                    t.date_deadline as date_deadline,
                    t.user_id,
                    t.phase_id,
                    t.project_id,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id as stage_id,
                    t.kanban_state as state,
                    t.working_days_close as working_days_close,
                    t.working_days_open  as working_days_open,
                    (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,
                    create_date,
                    write_date,
                   
                    date_end,
                    date_deadline,
                    date_last_stage_update,
                    t.user_id,
                    t.phase_id,
                    t.project_id,
                    t.priority,
                    name,
                    t.company_id,
                    t.partner_id,
                    stage_id
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM project_task t
                WHERE t.active = 'true'
                %s
        """ % (self._table, self._select(), self._group_by()))
    


