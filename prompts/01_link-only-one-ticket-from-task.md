---
title: "Link only one ticket from task"
state: completed
date_completed: 2026-09-22
model: moonshotai/Kimi-K2.6
input_tokens: 1067417
output_tokens: 18565
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

I have a working module `addons/project/helpdesk_project_task` that link tickets and
task. Currently it is a many2many link.

Replace this with many2one field. On a ticket only one task can be selected. On a task
it is one2many relationship to the ticket.

The smart button and tab on the ticket is no longer required. Instead the the `task_id`
should added before `project_id` on the form.

If a ticket is linked with a task the `sale_line_id` should computed with value from the
`task_id:sale_line_id`. Check the existing logic in
`enterprise/helpdesk_sale_timesheet/models/helpdesk_ticket.py`.

Consider bupming the module version and adding a migration script for ensuring the first
record of `task_ids` is used as new record for `task_id`.

## Worklog

- Replaced `project_task_ids` (Many2many) on `helpdesk.ticket` with `task_id`
  (Many2one).
- Replaced `helpdesk_ticket_ids` (Many2many) on `project.task` with
  `helpdesk_ticket_ids` (One2many, inverse `task_id`).
- Removed smart button and Tasks tab from the ticket form.
- Added `task_id` field before `project_id` in the ticket form via `helpdesk_timesheet`
  view inheritance.
- Overrode `_compute_sale_line_id` on `helpdesk.ticket` so linked tickets inherit
  `sale_line_id` from `task_id.sale_line_id`.
- Added `helpdesk_sale_timesheet` to module dependencies.
- Bumped module version to `18.0.2.0.0`.
- Created pre- and post-migration scripts in `migrations/18.0.2.0.0/` to migrate the
  first related task from the old relation table into the new `task_id` column.
- Updated `TEST_INSTRUCTIONS.rst` and frontmatter.
