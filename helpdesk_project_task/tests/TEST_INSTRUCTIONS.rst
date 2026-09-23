Linking a task to a ticket:

- Go to "Helpdesk > Tickets > All" tickets.
- Edit arbitrary ticket.
- Select a task in the "Task" field (before Project).

Timesheet propagation:

- Ensure the ticket is linked to a task.
- Add a timesheet entry to the ticket (e.g. via the timer or the Timesheets tab).
- Verify the timesheet entry is also linked to the task (task_id field).
- Try linking a timesheet to a ticket and a different task: this should raise an error.

Task field visibility and domain:

- The "Task" field is only visible when "Timesheet Invoicing" is enabled on the team AND the ticket has a partner set.
- The task dropdown only shows tasks that have a Sales Order Item (sale_line_id) AND whose partner is in the commercial partner hierarchy of the ticket's partner.

Sale order line propagation:

- Link a ticket to a task that has a Sales Order Item.
- Verify the ticket's "Sales Order Item" (sale_line_id) field shows the same value as the task.
