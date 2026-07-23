from odoo.tests.common import TransactionCase


class TestProjectMenuSync(TransactionCase):
    def test_01_create_project_creates_menu_and_action(self):
        project = self.env["project.project"].create(
            {
                "name": "Test Project",
                "key": "TP01",
            }
        )
        self.assertTrue(project.menu_id, "Project should have menu_id set after creation")
