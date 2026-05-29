import logging
from datetime import date

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _name = "project.estimate"
    _description = "Project Estimate"
    _rec_name = "phase_id"
    _order = "sequence"

    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    project_id = fields.Many2one("project.project")
    phase_id = fields.Many2one("project.task.phase", string="Project Phase")

    start_date = fields.Date(copy=False)
    end_date = fields.Date(copy=False)
    is_in_progress = fields.Boolean(
        compute="_compute_is_in_progress",
        store=True,
    )

    planned_hours = fields.Float()
    effective_hours = fields.Float(compute="_compute_effective_hours", compute_sudo=True, store=True)
    remaining_hours = fields.Float(compute="_compute_remaining_hours", store=True)

    progress = fields.Float(compute="_compute_progress_hours", store=True, group_operator="avg")
    effective_hours_validated = fields.Float(compute="_compute_effective_hours", compute_sudo=True, store=True)
    remaining_hours_validated = fields.Float(compute="_compute_remaining_hours", store=True)
    progress_validated = fields.Float(compute="_compute_progress_hours", store=True, group_operator="avg")

    @api.depends("start_date", "end_date")
    def _compute_is_in_progress(self):
        today = date.today()
        for record in self:
            if not record.start_date and not record.end_date:
                record.is_in_progress = True
            elif record.start_date and record.start_date <= today:
                record.is_in_progress = True
            elif record.end_date and record.end_date >= today:
                record.is_in_progress = True
            else:
                record.is_in_progress = False

    def _update_is_in_progress(self):
        """
        Daily cron job to update estimates with start or end date.
        """
        today = date.today()
        self.filtered(lambda e: e.end_date or e.start_date)._compute_is_in_progress()

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise models.ValidationError("End date cannot be before start date.")

    @api.depends(
        "project_id", "phase_id", "phase_id.task_ids", "phase_id.task_ids.effective_hours", "start_date", "end_date"
    )
    def _compute_effective_hours(self):
        for estimate in self:
            task_ids = (
                self.with_context(active_test=False)
                .env["project.task"]
                .search(
                    [
                        ("phase_id", "=", estimate.phase_id.id),
                        ("project_id", "=", estimate.project_id.id),
                    ]
                )
            )
            effective_hours = task_ids.timesheet_ids

            if estimate.start_date:
                effective_hours = effective_hours.filtered(lambda line: line.date >= estimate.start_date)

            if estimate.end_date:
                effective_hours = effective_hours.filtered(lambda line: line.date <= estimate.end_date)

            estimate.effective_hours = sum(effective_hours.mapped("unit_amount"))

            effective_hours_validated = effective_hours.filtered(lambda line: line.validated)
            estimate.effective_hours_validated = sum(effective_hours_validated.mapped("unit_amount"))

    @api.depends("planned_hours", "effective_hours")
    def _compute_remaining_hours(self):
        for estimate in self:
            estimate.remaining_hours = estimate.planned_hours - estimate.effective_hours
            estimate.remaining_hours_validated = estimate.planned_hours - estimate.effective_hours_validated

    @api.model
    def _calculate_progress(self, planned_hours, effective_hours):
        """
        Compare effective hours with planned hours.
        If planned hours is zero then set progress to 100%.
        When effective hours exceeds planned hours set progress to 100%.
        """
        progress = 0
        if planned_hours > 0.0:
            if (
                float_compare(
                    effective_hours,
                    planned_hours,
                    precision_digits=2,
                )
                >= 0
            ):
                progress = 100
            else:
                progress = round(100.0 * effective_hours / planned_hours, 2)
        else:
            progress = 100
        return progress

    @api.depends("remaining_hours")
    def _compute_progress_hours(self):
        for estimate in self:
            estimate.progress = self._calculate_progress(estimate.planned_hours, estimate.effective_hours)
            estimate.progress_validated = self._calculate_progress(
                estimate.planned_hours, estimate.effective_hours_validated
            )

    def action_open_timesheets(self):
        self.ensure_one()

        task_ids = self.env["project.task"].search(
            [
                ("phase_id", "=", self.phase_id.id),
                ("project_id", "=", self.project_id.id),
            ]
        )

        timesheet_domain = [("task_id", "in", task_ids.ids)]
        if self.start_date:
            timesheet_domain.append(("date", ">=", self.start_date))
        if self.end_date:
            timesheet_domain.append(("date", "<=", self.end_date))

        return {
            "type": "ir.actions.act_window",
            "name": "Timesheets for %s - %s" % (self.project_id.name, self.phase_id.name),
            "res_model": "account.analytic.line",
            "domain": timesheet_domain,
            "view_mode": "tree,form",
        }
