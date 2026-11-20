# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ProjectCostReportProduction(models.Model):
    _name = "project.cost.report.production"
    _description = "Project MO Report"
    _auto = False

    production_id = fields.Many2one(
        "mrp.production", string="Manufacturing Order", readonly=True
    )
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
                    mp.id,
                    mp.id AS production_id,
                    mp.project_id,
                    SUM(CASE WHEN wo.state IN ('done', 'cancel') THEN COALESCE(wo.duration, 0) / 60.0 ELSE 0 END) AS realised,
                    SUM(CASE WHEN wo.state = 'progress' THEN COALESCE(wo.duration, 0) / 60.0 ELSE 0 END) AS in_progress,
                    SUM(COALESCE(wo.duration_expected, 0) / 60.0) AS budget,
                    mp.company_id
                FROM mrp_production mp
                LEFT JOIN mrp_workorder wo ON wo.production_id = mp.id
                WHERE mp.project_id IS NOT NULL
                GROUP BY mp.id, mp.project_id, mp.company_id
            )
            """
        )
