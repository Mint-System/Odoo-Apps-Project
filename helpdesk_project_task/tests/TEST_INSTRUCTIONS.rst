Linking a task to a ticket:

- Go to "Helpdesk > Tickets > All" tickets.
- Edit arbitrary ticket.
- Select a task in the "Task" field (before Project).

Sale order line propagation:

- Enable "Timesheet Invoicing" on the Helpdesk Team (form: check "Re-Invoice Time").
- Ensure the task has a Sales Order Item (sale_line_id) set.
- Link a ticket to that task via the ticket form.
- Verify the ticket's "Sales Order Item" (sale_line_id) field shows the same value as the task.
- Remove the task link or change the task's SO line: the ticket should either clear or update accordingly.
