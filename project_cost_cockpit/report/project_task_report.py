# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ProjectCostReportTask(models.Model):
    _name = "project.cost.report.task"
    _description = "Project Task Report"
    _auto = False

    task_id = fields.Many2one("project.task", string="Task", readonly=True)
    project_id = fields.Many2one("project.project", string="Project", readonly=True)
    realised = fields.Float(readonly=True)
    in_progress = fields.Float(readonly=True)
    budget = fields.Float(readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            f"""
            CREATE VIEW {self._table} AS (
                SELECT
                    pt.id,
                    pt.id AS task_id,
                    pt.project_id,
                    SUM(CASE WHEN aal.timesheet_invoice_id IS NOT NULL THEN aal.unit_amount ELSE 0 END) AS realised,
                    SUM(COALESCE(aal.unit_amount, 0)) AS in_progress,
                    pt.allocated_hours AS budget,
                    pt.company_id
                FROM project_task pt
                LEFT JOIN account_analytic_line aal ON aal.task_id = pt.id
                WHERE pt.project_id IS NOT NULL AND pt.active = TRUE
                GROUP BY pt.id, pt.project_id, pt.allocated_hours, pt.company_id
            )
            """
        )
