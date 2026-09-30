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

    planned_date_begin = fields.Datetime("Start Date")
    planned_date_end = fields.Datetime("End Date")
    is_in_progress = fields.Boolean(
        compute="_compute_is_in_progress",
        store=True,
    )

    planned_hours = fields.Float()
    effective_hours = fields.Float(compute="_compute_effective_hours", compute_sudo=True, store=True)
    remaining_hours = fields.Float(compute="_compute_remaining_hours", store=True)

    progress = fields.Float(compute="_compute_progress_hours", store=True, aggregator="avg")
    effective_hours_validated = fields.Float(compute="_compute_effective_hours", compute_sudo=True, store=True)
    remaining_hours_validated = fields.Float(compute="_compute_remaining_hours", store=True)
    progress_validated = fields.Float(compute="_compute_progress_hours", store=True, aggregator="avg")

    def _local_date(self, value):
        """Convert a UTC datetime to a date in the user's timezone."""
        return fields.Date.context_today(self, value) if value else False

    @api.depends("planned_date_begin", "planned_date_end")
    def _compute_is_in_progress(self):
        today = date.today()
        for record in self:
            start_date = record._local_date(record.planned_date_begin)
            end_date = record._local_date(record.planned_date_end)
            if not start_date and not end_date:
                record.is_in_progress = True
            elif start_date and start_date <= today:
                record.is_in_progress = True
            elif end_date and end_date >= today:
                record.is_in_progress = True
            else:
                record.is_in_progress = False

    def _update_is_in_progress(self):
        """
        Daily cron job to update estimates with start or end date.
        """
        today = date.today()
        self.filtered(lambda e: e.planned_date_end or e.planned_date_begin)._compute_is_in_progress()

    @api.constrains("planned_date_begin", "planned_date_end")
    def _check_dates(self):
        for record in self:
            if (
                record.planned_date_begin
                and record.planned_date_end
                and record.planned_date_end < record.planned_date_begin
            ):
                raise models.ValidationError("End date cannot be before start date.")

    @api.depends(
        "project_id", "phase_id", "phase_id.task_ids", "phase_id.task_ids.effective_hours",
        "planned_date_begin",
        "planned_date_end",
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
            start_date = estimate._local_date(estimate.planned_date_begin)
            end_date = estimate._local_date(estimate.planned_date_end)

            if start_date:
                effective_hours = effective_hours.filtered(lambda line: line.date >= start_date)

            if end_date:
                effective_hours = effective_hours.filtered(lambda line: line.date <= end_date)

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
        start_date = self._local_date(self.planned_date_begin)
        end_date = self._local_date(self.planned_date_end)
        if start_date:
            timesheet_domain.append(("date", ">=", start_date))
        if end_date:
            timesheet_domain.append(("date", "<=", end_date))

        return {
            "type": "ir.actions.act_window",
            "name": "Timesheets for %s - %s" % (self.project_id.name, self.phase_id.name),
            "res_model": "account.analytic.line",
            "domain": timesheet_domain,
            "view_mode": "list,form",
        }