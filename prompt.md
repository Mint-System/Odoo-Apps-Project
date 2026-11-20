---
title: "new module test project cost reporting"
author: "laurens kooijman <laurenskooijman@gmail.com>"
session_id: "01a1f87a-35c3-7223-90e7-c370df291cc9"
action: execute
state: review
date_completed: YYYY-MM-DD
harness: pi
provider: moonshotai
model: moonshotai/Kimi-K2.6
input_tokens: 106600
output_tokens: 56652
---

# new module test project cost reporting

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` to get an understanding of the project
- Read task section and prepare a list of todos
- Update the todo list while working on task

## Task


Create a series of reports that are linked with each other by clicking in the entries. Use the module `project_cost_cockpit` in addons/project to add the reports to. Look into the existing report to see how the work order can be queried with SQL.

This should be the order and content of the reports. The values (columns) I will define below:
1: Name 'project_report'. Pivot table with one line per project. On click on project line go to report 2/project_individual_report.
2: Name 'project_individual_report'. The project that is clicked on in the previous report, a pivot view with tasks and manufacturing orders that are linked to that project (field project_id in Task and MO). On click on task line: Go to task. On click on MO line, go to MO.

For pivot 2, it will be complicated to show tasks and MOs on the same Pivot. First find the right way to do that. Perhaps it is easier to to aggregate MOs and tasks and only see individual tasks/MOs after clicking on that line. Then make that the third level. This level would be two reports, for MOs and Tasks, the names would be project_mo_report and project_task_report.

I always want to have these values in the Pivot tables:
- Realised
- In progress
- Budget

For MOs this means looking into the work orders (mrp.workorder):
- Realised = timesheet costs related to work orders in state 'done' or 'cancel'.
- In progress = timesheet costs related to work orders in state 'progress'.
- Budget = sum of the field duration_expected for all workorders multiplied by a value of 80 per hour.  

For tasks this means looking into timesheet entries:
- Realised = timesheet_invoice_id is set
- In progress = all timesheet durations on that task.
- Budget = the field 'allocated_hours'


@Clanker When task is completed set frontmatter state to review. If you have access to session info add token count and session id. Prompt the author to verify the results.

## Worklog

Created four linked reporting views in the `project_cost_cockpit` module:

1. **project_report** (`project.cost.report.project`) — One row per project. Measures are now in **hours**:
   - Realised = task invoiced hours + MO done/cancel hours
   - In Progress = task all hours + MO in-progress hours
   - Budget = task allocated_hours + MO expected hours

2. **project_individual_report** (`project.cost.report.type`) — Two rows per project:
   - **Tasks** — hours (realised=invoiced, in_progress=all, budget=allocated_hours)
   - **Manufacturing Orders** — working hours only (realised=done/cancel duration, in_progress=progress duration, budget=duration_expected)

3. **project_task_report** (`project.cost.report.task`) — One row per task with hours.

4. **project_mo_report** (`project.cost.report.production`) — One row per MO with working hours (duration instead of costs).

Changes made:
- Added `sale_timesheet` dependency to `__manifest__.py`.
- Created SQL view models using direct `mrp_workorder.duration` / `duration_expected` for hours (not analytic line costs).
- Custom JS (`project_report_pivot.js`) enables cross-model pivot click-through navigation.
- Added pivot, list, and search views; all hour fields use `widget="float_time"` for HH:MM display.
- Added model access rules in `security/ir.model.access.csv`.
- Added menu items under Project > Reporting.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info update token count. Finally, update the changelog with the most important changes.
