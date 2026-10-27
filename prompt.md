---
title: "New module project update list"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
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

Create a new module `project_update_list` in this folder.

The summary is "Prepare multiple project updates from kanban phase or list view."

This module adds a list view for `project.update` and a menu entry to access project updates.

It adds a field `batch` (char) to the `project.update` model.

The rows are project, customer, project manager, phase, state, date and description.

Further it adds an action `prepare_project_update` to `project.project`. This action shows a prompt to enter a batch name.
It suggest the current year and week `2026W07` and confirmation generates a `project.upate` record for each selected project.
It then clears the description and shows the list.

When user opens the list the default group `batch` is applied and expanded. The user can directly edit phase, state, date and description in the list view.
In the list view is a additional button `View` that opens the task board of the project.

The list is sorted by batch and then by project manager.

Create tests for these features.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
