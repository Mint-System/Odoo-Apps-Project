---
title: "Add date picker to prepare update dialog"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2025-06-10
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 70573
output_tokens: 15590
---

# Add date picker to prepare update dialog

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

The `addons/project/project_update_list/wizard/prepare_project_update_wizard.py` wizard
should provide a date picker.

The selected date is used as date for the project update entries. Also the the batch
name / week number is computed based on the date.

Update tests.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

- Added `date` field (`fields.Date`) to `prepare.project.update.wizard` with a default
  of today.
- Replaced `@api.onchange` with a `compute="_compute_batch"` field on `batch` so
  changing the date updates the batch name automatically. The compute uses the ISO
  week of the selected date (`YYYY-WNN` format). `readonly=False` allows manual
  override.
- Updated `action_prepare` to pass the wizard's `date` to each created `project.update`
  record.
- Updated the wizard form view (`prepare_project_update_wizard_views.xml`) to show the
  date picker above the batch field.
- Updated `tests/test_project_update_list.py`:
  - Added test verifying the default date is today.
  - Added test verifying the default batch matches the default date's ISO week.
  - Added test verifying `_compute_batch` computes the correct batch from date.
  - Added test verifying created project updates use the wizard's selected date.
  - Updated existing tests to include a date when creating the wizard.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
