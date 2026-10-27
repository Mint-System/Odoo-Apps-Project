---
title: "New module project update list"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-27
harness:
model:
input_tokens:
output_tokens:
---

# New module project update list

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

### Module

Create a new module `project_update_list` in this folder.

The summary is "Prepare multiple project updates from kanban phase or list view."

This module adds a list view for `project.update` and a menu entry to access project
updates.

It adds a field `batch` (char) to the `project.update` model.

The rows are project, customer, project manager, phase, state, date and description.

Further it adds an action `prepare_project_update` to `project.project`. This action
shows a prompt to enter a batch name. It suggest the current year and week `2026W07` and
confirmation generates a `project.update` record for each selected project. It then
clears the description and shows the list.

When user opens the list the default group `batch` is applied and expanded. The user can
directly edit phase, state, date and description in the list view.

In the list view is a additional button `View` that opens the task board of the project.
Then there is also delete icon that allows deleting a project update. Both buttons are
hidden by default.

The list is sorted by batch and then by project manager.

### Generate

Use the `create-module` and `generate-module-*` commands to bootstrap the module.

### Testing

Create tests for these prepare method.

Use the `init-module` command to install. I will then preview / test the functionality.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

Created module `project_update_list` in `addons/project/project_update_list`.

### Implementation summary

- **Models:**

  - Inherited `project.update` to add `batch` (Char), `partner_id` (related to project
    customer, stored), and `project_user_id` (related to project manager, stored). Added
    custom `_order` for batch + project manager sorting.
  - Inherited `project.project` with helper action.
  - Added `prepare.project.update.wizard` transient model that suggests current
    year/week as batch default and creates one `project.update` per selected project.

- **Views & Actions:**

  - Created a dedicated editable tree view for `project.update` with inline editing.
  - Added search view group-by filter for `batch`.
  - Added `Prepare Project Update` action (gear menu + stat button on project form) that
    opens the wizard.
  - Added menu entry `Project Updates` under the Project app.

- **Tests:**
  - `test_default_batch_format`: verifies wizard default batch is `YYYYWNN`.
  - `test_action_prepare_creates_updates`: verifies one update per selected project and
    correct return action.
  - `test_action_prepare_clears_description`: verifies created updates have no
    description.
  - `test_create_sets_name_from_batch`: verifies `project.update` name defaults to batch
    when omitted.

All tests pass. Module installed successfully with `task init-module` and
`task test-module`.

### Author verification

Please verify the results. Set frontmatter state to `completed` or `aborted`.
