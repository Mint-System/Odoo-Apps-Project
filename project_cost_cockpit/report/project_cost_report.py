# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ProjectCostReport(models.Model):
    _name = "project.cost.report"
    _description = "Project Cost Cockpit"
    _order = "date desc, project_id"
    _auto = False

    project_id = fields.Many2one("project.project", string="Project", readonly=True)
    date = fields.Date(readonly=True)
    timesheet_cost = fields.Monetary(readonly=True)
    manufacturing_operation_cost = fields.Monetary(readonly=True)
    manufacturing_component_cost = fields.Monetary(readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)
    currency_id = fields.Many2one(related="company_id.currency_id")

    def _select(self):
        return """
            MIN(aal.id) AS id,
            COALESCE(pp_direct.id, pp_account.id) AS project_id,
            DATE_TRUNC('month', aal.date)::date AS date,
            SUM(CASE
                WHEN sm_rel.account_analytic_line_id IS NOT NULL
                  AND sm.raw_material_production_id IS NOT NULL
                THEN -aal.amount ELSE 0
            END) AS manufacturing_component_cost,
            SUM(CASE
                WHEN wo_mo_rel.account_analytic_line_id IS NOT NULL
                  OR wo_wc_rel.account_analytic_line_id IS NOT NULL
                  OR wo_emp_rel.account_analytic_line_id IS NOT NULL
                THEN -aal.amount ELSE 0
            END) AS manufacturing_operation_cost,
            SUM(CASE
                WHEN aal.project_id IS NOT NULL
                  AND sm_rel.account_analytic_line_id IS NULL
                  AND wo_mo_rel.account_analytic_line_id IS NULL
                  AND wo_wc_rel.account_analytic_line_id IS NULL
                  AND wo_emp_rel.account_analytic_line_id IS NULL
                THEN -aal.amount ELSE 0
            END) AS timesheet_cost,
            COALESCE(pp_direct.company_id, pp_account.company_id) AS company_id
        """

    def _from(self):
        return """
            account_analytic_line aal
        """

    def _join(self):
        return """
            LEFT JOIN project_project pp_direct ON pp_direct.id = aal.project_id
            LEFT JOIN project_project pp_account ON pp_account.account_id = aal.account_id
            LEFT JOIN account_analytic_line_stock_move_rel sm_rel ON sm_rel.account_analytic_line_id = aal.id
            LEFT JOIN stock_move sm ON sm.id = sm_rel.stock_move_id
            LEFT JOIN mrp_workorder_mo_analytic_rel wo_mo_rel ON wo_mo_rel.account_analytic_line_id = aal.id
            LEFT JOIN mrp_workorder_wc_analytic_rel wo_wc_rel ON wo_wc_rel.account_analytic_line_id = aal.id
            LEFT JOIN account_analytic_line_mrp_workorder_rel wo_emp_rel ON wo_emp_rel.account_analytic_line_id = aal.id
        """

    def _where(self):
        return "pp_direct.id IS NOT NULL OR pp_account.id IS NOT NULL"

    def _group_by(self):
        return """
            COALESCE(pp_direct.id, pp_account.id),
            DATE_TRUNC('month', aal.date)::date,
            COALESCE(pp_direct.company_id, pp_account.company_id)
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE VIEW %s AS (
                SELECT %s
                FROM %s
                %s
                WHERE %s
                GROUP BY %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where(), self._group_by()))
