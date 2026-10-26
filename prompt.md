---
title: "Bugfix Project Phase Estimate"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
---

# Bugfix Project Phase Estimate

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I have multiple bugfixes and improvements for `project_phase_estimate`. Try to identify the bugs in the code and create a solution.

### Bug: is_running computes True if start and end date are past

If past start date is removed and end date to a past date then it computes to false, which would be correct.

### Bug: On task show phase and percentage for estimates with is_running true

Currently it calculates estimate progress based on all estimates, but it should only consider estimates with `is_running` true.

The selection of phases should be phases with is_running estimates only.

### Bug: Cron job "Project: Update project estimates" does not work

Maybe related to "is_running compute bug"

### Bug: Archived projects do not archive estimates

Make the archive action of projects cascade into estimates.

### Inherit project phase on subtasks

When creating a subtask apply the same phase from parent to the task.

### Add project_id to context

When I click on phase_id from task and then on smart-button for estimates, all estimates are shown.

Instead the project_id should be passed as context and then applied as filter `default_filter_*` to the estimates list.

### Show phase_id field before user_ids field

On task with `parent_id` the `phase_id` comes before the `display_project_id`. To make the ui consisten place the `phase_id` before `user_ids`.

### Testing

There is a `addons/project/project_phase_estimate/tests/TEST_INSTRUCTIONS.rst` containing manual instructions. I am asking you to implement this as actual Python tests.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
