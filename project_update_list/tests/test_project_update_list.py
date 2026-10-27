# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProjectUpdateList(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.project2 = cls.env["project.project"].create({"name": "Test Project 2"})

    def test_default_batch_format(self):
        """Wizard defaults batch to current year and week."""
        wizard = self.env["prepare.project.update.wizard"].create({})
        today = wizard.default_get(["batch"]).get("batch")
        self.assertRegex(today, r"^\d{4}W\d{2}$")

    def test_action_prepare_creates_updates(self):
        """Prepare action creates a project update per selected project."""
        wizard = self.env["prepare.project.update.wizard"].create({"batch": "2026W07"})
        ctx = {
            "active_ids": [self.project.id, self.project2.id],
            "active_model": "project.project",
        }
        result = wizard.with_context(**ctx).action_prepare()

        updates = self.env["project.update"].search([("batch", "=", "2026W07")])
        self.assertEqual(len(updates), 2)
        self.assertEqual(result["res_model"], "project.update")
        self.assertEqual(result["domain"], [("batch", "=", "2026W07")])

    def test_action_prepare_clears_description(self):
        """New updates have no description."""
        wizard = self.env["prepare.project.update.wizard"].create({"batch": "2026W07"})
        ctx = {
            "active_ids": [self.project.id],
            "active_model": "project.project",
        }
        wizard.with_context(**ctx).action_prepare()

        update = self.env["project.update"].search([("batch", "=", "2026W07"), ("project_id", "=", self.project.id)])
        self.assertFalse(update.description)

    def test_create_sets_name_from_batch(self):
        """Creating an update with batch but no name defaults name to 'Project Status'."""
        update = self.env["project.update"].create(
            {
                "project_id": self.project.id,
                "batch": "2026W07",
                "status": "on_track",
            }
        )
        self.assertEqual(update.name, "Project Status")
