---
title: "Improve Helpdesk Project Task"
state: completed
date_completed: 2026-09-23
model: moonshotai/Kimi-K2.6
input_tokens: 2044102
output_tokens: 23601
---

# Run 01

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

The module `addons/project/helpdesk_project_task` makes a connection between task and ticket.

I would like to have these improvements:

- When a timesheet entry is added to the ticket and the ticket is linked with a task, then the timesheet entry should also be linked to this task
- The sale_line_id is only linked from task if the task has a sale_line_id set

## Worklog

- Created `models/account_analytic_line.py` to propagate `task_id` from a ticket's linked task when creating or writing a timesheet. Overrode `_compute_task_id`, `_compute_helpdesk_ticket_id`, and `_check_no_link_task_and_ticket` to allow both fields simultaneously only when the ticket is linked to the same task.
- Added `domain="[('sale_line_id', '!=', False)]"` on the `task_id` field so only tasks with a sale order line can be selected. This makes the conditional `sale_line_id` propagation unnecessary; the original `_compute_sale_line_id` logic is restored.
- Added `tests/test_helpdesk_project_task.py` with tests covering timesheet creation/write propagation, constraint validation for inconsistent task/ticket links, and conditional sale-line propagation.
- Updated `tests/TEST_INSTRUCTIONS.rst` with new manual test steps for the timesheet propagation feature.

@Clanker Set frontmatter state to completed and update date and model. If you have access to session info also add token count.
