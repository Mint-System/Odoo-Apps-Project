# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.tools import date_utils


class TestProjectUpdateList(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.project2 = cls.env["project.project"].create({"name": "Test Project 2"})

    def test_default_date(self):
        """Wizard defaults date to today."""
        defaults = self.env["prepare.project.update.wizard"].default_get(["date", "batch"])
        today = date_utils.date_today()
        self.assertEqual(defaults.get("date"), today)

    def test_default_batch_from_date(self):
        """Batch is computed from the default date."""
        wizard = self.env["prepare.project.update.wizard"].create({})
        date = wizard.date
        expected = f"{date.strftime('%Y')}-W{date.isocalendar()[1]:02d}"
        self.assertEqual(wizard.batch, expected)

    def test_batch_computed_from_date(self):
        """Batch reflects the ISO week of the selected date."""
        date = self.env["prepare.project.update.wizard"]._fields["date"].to_date("2025-06-10")
        wizard = self.env["prepare.project.update.wizard"].create({"date": date})
        self.assertEqual(wizard.batch, "2025-W24")

    def test_action_prepare_creates_updates(self):
        """Prepare action creates a project update per selected project."""
        date = self.env["prepare.project.update.wizard"]._fields["date"].to_date("2026-02-10")
        wizard = self.env["prepare.project.update.wizard"].create({"date": date, "batch": "2026-W07"})
        ctx = {
            "active_ids": [self.project.id, self.project2.id],
            "active_model": "project.project",
        }
        result = wizard.with_context(**ctx).action_prepare()

        updates = self.env["project.update"].search([("batch", "=", "2026-W07")])
        self.assertEqual(len(updates), 2)
        self.assertEqual(result["res_model"], "project.update")
        self.assertEqual(result["domain"], [("batch", "=", "2026-W07")])

    def test_action_prepare_uses_selected_date(self):
        """Created updates use the wizard's selected date."""
        date = self.env["prepare.project.update.wizard"]._fields["date"].to_date("2026-02-10")
        wizard = self.env["prepare.project.update.wizard"].create({"date": date, "batch": "2026-W07"})
        ctx = {
            "active_ids": [self.project.id],
            "active_model": "project.project",
        }
        wizard.with_context(**ctx).action_prepare()

        update = self.env["project.update"].search([("batch", "=", "2026-W07"), ("project_id", "=", self.project.id)])
        self.assertEqual(update.date, date)

    def test_action_prepare_clears_description(self):
        """New updates have no description."""
        date = self.env["prepare.project.update.wizard"]._fields["date"].to_date("2026-02-10")
        wizard = self.env["prepare.project.update.wizard"].create({"date": date, "batch": "2026-W07"})
        ctx = {
            "active_ids": [self.project.id],
            "active_model": "project.project",
        }
        wizard.with_context(**ctx).action_prepare()

        update = self.env["project.update"].search([("batch", "=", "2026-W07"), ("project_id", "=", self.project.id)])
        self.assertFalse(update.description)

    def test_create_sets_name_from_batch(self):
        """Creating an update with batch but no name defaults name to 'Project Status'."""
        update = self.env["project.update"].create(
            {
                "project_id": self.project.id,
                "batch": "2026-W07",
                "status": "on_track",
            }
        )
        self.assertEqual(update.name, "Project Status")
