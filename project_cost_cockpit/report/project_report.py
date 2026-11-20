# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ProjectCostReportProject(models.Model):
    _name = "project.cost.report.project"
    _description = "Project Report"
    _auto = False

    project_id = fields.Many2one("project.project", string="Project", readonly=True)
    realised = fields.Float(readonly=True)
    in_progress = fields.Float(readonly=True)
    budget = fields.Float(readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)

    def action_open_individual_report(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Project Individual Report",
            "res_model": "project.cost.report.type",
            "view_mode": "pivot",
            "views": [(False, "pivot")],
            "target": "current",
            "context": {
                "search_default_project_id": self.project_id.id,
            },
        }

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            f"""
            CREATE VIEW {self._table} AS (
                SELECT
                    pp.id,
                    pp.id AS project_id,
                    COALESCE(td.task_realised, 0.0) + COALESCE(md.mo_realised, 0.0) AS realised,
                    COALESCE(td.task_in_progress, 0.0) + COALESCE(md.mo_in_progress, 0.0) AS in_progress,
                    COALESCE(td.task_budget, 0.0) + COALESCE(md.mo_budget, 0.0) AS budget,
                    pp.company_id
                FROM project_project pp
                LEFT JOIN (
                    SELECT
                        pt.project_id,
                        SUM(CASE WHEN aal.timesheet_invoice_id IS NOT NULL THEN aal.unit_amount ELSE 0 END) AS task_realised,
                        SUM(COALESCE(aal.unit_amount, 0)) AS task_in_progress,
                        SUM(pt.allocated_hours) AS task_budget
                    FROM project_task pt
                    LEFT JOIN account_analytic_line aal ON aal.task_id = pt.id
                    WHERE pt.project_id IS NOT NULL AND pt.active = TRUE
                    GROUP BY pt.project_id
                ) td ON td.project_id = pp.id
                LEFT JOIN (
                    SELECT
                        mp.project_id,
                        SUM(CASE WHEN wo.state IN ('done', 'cancel') THEN COALESCE(wo.duration, 0) / 60.0 ELSE 0 END) AS mo_realised,
                        SUM(CASE WHEN wo.state = 'progress' THEN COALESCE(wo.duration, 0) / 60.0 ELSE 0 END) AS mo_in_progress,
                        SUM(COALESCE(wo.duration_expected, 0) / 60.0) AS mo_budget
                    FROM mrp_production mp
                    LEFT JOIN mrp_workorder wo ON wo.production_id = mp.id
                    WHERE mp.project_id IS NOT NULL
                    GROUP BY mp.project_id
                ) md ON md.project_id = pp.id
                WHERE pp.active = TRUE
            )
            """
        )
