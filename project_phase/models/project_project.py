from odoo import api, fields, models, _, tools


class ProjectProject(models.Model):
    _inherit='project.project'
    
    project_phase_count = fields.Integer('Job Note', compute='_compute_get_project_phase_count')

    def _compute_get_project_phase_count    (self):
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
    _description = "Tasks Analysis"

    phase_id = fields.Many2one('project.task.phase', string='Project Phase', readonly=True)


    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                    t.id as task_id,
                    t.create_date as create_date,
                    t.date_assign as date_assign,
                    t.date_end as date_end,
                    t.date_last_stage_update as date_last_stage_update,
                    t.date_deadline as date_deadline,
                    t.project_id,
                    t.phase_id,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id as stage_id,
                    t.kanban_state as state,
                    NULLIF(t.rating_last_value, 0) as rating_last_value,
                    t.working_days_close as working_days_close,
                    t.working_days_open  as working_days_open,
                    t.working_hours_open as working_hours_open,
                    t.working_hours_close as working_hours_close,
                    (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        """
        return select_str


    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,
                    t.create_date,
                    t.write_date,
                    t.date_assign,
                    t.date_end,
                    t.date_deadline,
                    t.date_last_stage_update,
                    t.project_id,
                    t.phase_id,
                    t.priority,
                    t.name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM project_task t
              LEFT JOIN project_task_user_rel tu on t.id=tu.task_id
                WHERE t.active = 'true'
                %s
        """ % (self._table, self._select(), self._group_by()))
