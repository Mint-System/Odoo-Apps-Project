from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestProjectPhaseEstimate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.phase = cls.env["project.task.phase"].create({"name": "Test Phase"})
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
                "phase_id": cls.phase.id,
            }
        )

    def test_is_in_progress_no_dates(self):
        """Estimate without dates is always in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
            }
        )
        self.assertTrue(estimate.is_in_progress)

    def test_is_in_progress_past_start_no_end(self):
        """Estimate with past start date and no end date is in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() - timedelta(days=10),
            }
        )
        self.assertTrue(estimate.is_in_progress)

    def test_is_in_progress_future_start_no_end(self):
        """Estimate with future start date and no end date is not in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() + timedelta(days=10),
            }
        )
        self.assertFalse(estimate.is_in_progress)

    def test_is_in_progress_no_start_future_end(self):
        """Estimate with no start date and future end date is in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "end_date": fields.Date.today() + timedelta(days=10),
            }
        )
        self.assertTrue(estimate.is_in_progress)

    def test_is_in_progress_no_start_past_end(self):
        """Estimate with no start date and past end date is not in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "end_date": fields.Date.today() - timedelta(days=10),
            }
        )
        self.assertFalse(estimate.is_in_progress)

    def test_is_in_progress_both_dates_current(self):
        """Estimate with dates spanning today is in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() - timedelta(days=5),
                "end_date": fields.Date.today() + timedelta(days=5),
            }
        )
        self.assertTrue(estimate.is_in_progress)

    def test_is_in_progress_both_dates_past(self):
        """Estimate with both start and end dates in the past is not in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() - timedelta(days=10),
                "end_date": fields.Date.today() - timedelta(days=5),
            }
        )
        self.assertFalse(estimate.is_in_progress)

    def test_is_in_progress_both_dates_future(self):
        """Estimate with both start and end dates in the future is not in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() + timedelta(days=5),
                "end_date": fields.Date.today() + timedelta(days=10),
            }
        )
        self.assertFalse(estimate.is_in_progress)

    def test_is_in_progress_past_start_removed_past_end(self):
        """Removing past start date from estimate with past end date sets not in progress."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() - timedelta(days=10),
                "end_date": fields.Date.today() - timedelta(days=5),
            }
        )
        self.assertFalse(estimate.is_in_progress)
        estimate.start_date = False
        self.assertFalse(estimate.is_in_progress)

    def test_task_estimate_id_only_running(self):
        """Task estimate_id should link to in-progress estimate."""
        phase2 = self.env["project.task.phase"].create({"name": "Running Phase"})
        task = self.env["project.task"].create(
            {
                "name": "Running Task",
                "project_id": self.project.id,
                "phase_id": phase2.id,
            }
        )
        self.assertTrue(task.estimate_id.is_in_progress)
        self.assertEqual(task.estimate_id.phase_id, phase2)

    def test_cron_updates_is_in_progress(self):
        """Cron job should update is_in_progress for estimates with dates."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "start_date": fields.Date.today() + timedelta(days=1),
                "end_date": fields.Date.today() + timedelta(days=10),
            }
        )
        self.assertFalse(estimate.is_in_progress)
        estimate.start_date = fields.Date.today() - timedelta(days=1)
        estimate.end_date = fields.Date.today() + timedelta(days=5)
        self.env["project.estimate"]._update_is_in_progress()
        self.assertTrue(estimate.is_in_progress)

    def test_archive_project_archives_estimates(self):
        """Archiving a project should archive its estimates."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
            }
        )
        self.assertTrue(estimate.active)
        self.project.write({"active": False})
        self.assertFalse(estimate.active)

    def test_subtask_inherits_parent_phase(self):
        """Creating a subtask should inherit the parent's phase."""
        parent_task = self.env["project.task"].create(
            {
                "name": "Parent Task",
                "project_id": self.project.id,
                "phase_id": self.phase.id,
            }
        )
        subtask = self.env["project.task"].create(
            {
                "name": "Subtask",
                "project_id": self.project.id,
                "parent_id": parent_task.id,
            }
        )
        self.assertEqual(subtask.phase_id, self.phase)

    def test_subtask_explicit_phase_not_overridden(self):
        """Creating a subtask with explicit phase should keep the explicit phase."""
        parent_task = self.env["project.task"].create(
            {
                "name": "Parent Task",
                "project_id": self.project.id,
                "phase_id": self.phase.id,
            }
        )
        other_phase = self.env["project.task.phase"].create({"name": "Other Phase"})
        subtask = self.env["project.task"].create(
            {
                "name": "Subtask",
                "project_id": self.project.id,
                "parent_id": parent_task.id,
                "phase_id": other_phase.id,
            }
        )
        self.assertEqual(subtask.phase_id, other_phase)

    def test_phase_action_project_estimate_with_project_context(self):
        """Phase estimate action should filter by project when default_project_id is in context."""
        action = self.phase.with_context(default_project_id=self.project.id).action_project_estimate()
        self.assertIn(("project_id", "=", self.project.id), action["domain"])
        self.assertEqual(action["context"]["search_default_project_id"], self.project.id)

    def test_phase_action_project_estimate_without_project_context(self):
        """Phase estimate action should not filter by project without default_project_id."""
        action = self.phase.action_project_estimate()
        self.assertNotIn(("project_id", "=", self.project.id), action["domain"])

    def test_effective_hours_filtered_by_dates(self):
        """Effective hours should be filtered by estimate start and end dates."""
        employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "user_id": self.env.user.id,
            }
        )
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "planned_hours": 20,
                "start_date": fields.Date.today() - timedelta(days=6),
                "end_date": fields.Date.today(),
            }
        )
        # Create timesheets within date range
        self.env["account.analytic.line"].create(
            {
                "name": "Within range",
                "project_id": self.project.id,
                "task_id": self.task.id,
                "date": fields.Date.today() - timedelta(days=3),
                "unit_amount": 5,
                "employee_id": employee.id,
            }
        )
        # Create timesheet outside date range
        self.env["account.analytic.line"].create(
            {
                "name": "Outside range",
                "project_id": self.project.id,
                "task_id": self.task.id,
                "date": fields.Date.today() - timedelta(days=10),
                "unit_amount": 3,
                "employee_id": employee.id,
            }
        )
        self.assertEqual(estimate.effective_hours, 5)

    def test_estimate_project_phase_unique_constraint(self):
        """Creating two in-progress estimates with the same project and phase should raise an error."""
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "planned_hours": 10,
            }
        )
        with self.assertRaises(Exception):
            self.env["project.estimate"].create(
                {
                    "project_id": self.project.id,
                    "phase_id": self.phase.id,
                    "planned_hours": 20,
                }
            )

    def test_phase_estimate_count_in_progress(self):
        """Phase estimate count should only count in-progress estimates."""
        # Trigger auto-creation of the in-progress estimate from setUpClass
        self.task.estimate_id
        phase2 = self.env["project.task.phase"].create({"name": "Not Running Phase"})
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": phase2.id,
                "end_date": fields.Date.today() - timedelta(days=5),
            }
        )
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "end_date": fields.Date.today() - timedelta(days=5),
            }
        )
        self.assertEqual(phase2.estimate_count, 1)
        self.assertEqual(phase2.estimate_in_progress_count, 0)
        self.assertEqual(self.phase.estimate_count, 2)
        self.assertEqual(self.phase.estimate_in_progress_count, 1)
