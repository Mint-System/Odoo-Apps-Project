from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo.addons.helpdesk_timesheet.tests.common import TestHelpdeskTimesheetCommon


@tagged("-at_install", "post_install")
class TestHelpdeskProjectTask(TestHelpdeskTimesheetCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product = cls.env["product.product"].create({
            "name": "Service",
            "type": "service",
            "lst_price": 100.0,
        })
        order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
            "order_line": [(0, 0, {"product_id": product.id, "product_uom_qty": 1})],
        })
        order.action_confirm()
        cls.sale_line = order.order_line[0]
        cls.task = cls.env["project.task"].create({
            "name": "Test Task",
            "project_id": cls.project.id,
            "partner_id": cls.partner.id,
            "sale_line_id": cls.sale_line.id,
        })

    def test_timesheet_linked_to_task_via_ticket(self):
        """A timesheet created on a ticket that is linked to a task inherits the task."""
        timesheet = self.env["account.analytic.line"].create({
            "name": "Test Timesheet",
            "unit_amount": 1,
            "project_id": self.project.id,
            "helpdesk_ticket_id": self.helpdesk_ticket.id,
            "employee_id": self.empl_employee.id,
        })
        self.assertFalse(timesheet.task_id, "Timesheet should not have a task when ticket has none")

        self.helpdesk_ticket.task_id = self.task
        timesheet2 = self.env["account.analytic.line"].create({
            "name": "Test Timesheet 2",
            "unit_amount": 1,
            "project_id": self.project.id,
            "helpdesk_ticket_id": self.helpdesk_ticket.id,
            "employee_id": self.empl_employee.id,
        })
        self.assertEqual(timesheet2.task_id, self.task, "Timesheet should be linked to the ticket's task")

    def test_timesheet_write_helpdesk_ticket_with_task(self):
        """Writing helpdesk_ticket_id to a ticket that has a task sets task_id."""
        self.helpdesk_ticket.task_id = self.task
        timesheet = self.env["account.analytic.line"].create({
            "name": "Test Timesheet",
            "unit_amount": 1,
            "project_id": self.project.id,
            "employee_id": self.empl_employee.id,
        })
        self.assertFalse(timesheet.helpdesk_ticket_id)
        self.assertFalse(timesheet.task_id)

        timesheet.write({"helpdesk_ticket_id": self.helpdesk_ticket.id})
        self.assertEqual(timesheet.task_id, self.task, "Task should be set after linking ticket")

    def test_timesheet_constraint_task_and_ticket(self):
        """Constraint allows both fields when the ticket is linked to the same task."""
        self.helpdesk_ticket.task_id = self.task

        timesheet = self.env["account.analytic.line"].create({
            "name": "Valid Timesheet",
            "unit_amount": 1,
            "project_id": self.project.id,
            "helpdesk_ticket_id": self.helpdesk_ticket.id,
            "task_id": self.task.id,
            "employee_id": self.empl_employee.id,
        })
        self.assertTrue(timesheet)
        self.assertEqual(timesheet.task_id, self.task)
        self.assertEqual(timesheet.helpdesk_ticket_id, self.helpdesk_ticket)

        other_task = self.env["project.task"].create({
            "name": "Other Task",
            "project_id": self.project.id,
        })
        with self.assertRaises(ValidationError):
            self.env["account.analytic.line"].create({
                "name": "Invalid Timesheet",
                "unit_amount": 1,
                "project_id": self.project.id,
                "helpdesk_ticket_id": self.helpdesk_ticket.id,
                "task_id": other_task.id,
                "employee_id": self.empl_employee.id,
            })

    def test_sale_line_id_propagation_from_task(self):
        """sale_line_id is propagated from the linked task."""
        self.helpdesk_team.write({"use_helpdesk_sale_timesheet": True})
        self.helpdesk_ticket.task_id = self.task
        self.helpdesk_ticket._compute_sale_line_id()
        self.assertEqual(self.helpdesk_ticket.sale_line_id, self.sale_line)

    def test_sale_line_id_no_propagation_when_task_has_none(self):
        """When the task has no sale_line_id, the ticket falls back to standard logic."""
        self.helpdesk_team.write({"use_helpdesk_sale_timesheet": True})
        self.helpdesk_ticket.task_id = self.task
        self.task.sale_line_id = False
        self.helpdesk_ticket._compute_sale_line_id()
        self.assertFalse(self.helpdesk_ticket.sale_line_id)
