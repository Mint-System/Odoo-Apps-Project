---
commit_ref: a2354226a7586ebae7a769dbb397c5ef21ecd60b
title: "Bugfix Project Phase Estimate"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-26
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 12387699
output_tokens: 160411
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

I have multiple bugfixes and improvements for `project_phase_estimate`. Try to identify
the bugs in the code and create a solution.

### Bug: is_running computes True if start and end date are past

If past start date is removed and end date to a past date then it computes to false,
which would be correct.

### Bug: On task show phase and percentage for estimates with is_running true

Currently it calculates estimate progress based on all estimates, but it should only
consider estimates with `is_running` true.

The selection of phases should be phases with is_running estimates only.

### Bug: Cron job "Project: Update project estimates" does not work

Maybe related to "is_running compute bug"

### Bug: Archived projects do not archive estimates

Make the archive action of projects cascade into estimates.

### Inherit project phase on subtasks

When creating a subtask apply the same phase from parent to the task.

### Add project_id to context

When I click on phase_id from task and then on smart-button for estimates, all estimates
are shown.

Instead the project*id should be passed as context and then applied as filter
`default_filter*\*` to the estimates list.

### Show phase_id field before user_ids field

On task with `parent_id` the `phase_id` comes before the `display_project_id`. To make
the ui consisten place the `phase_id` before `user_ids`.

### Testing

There is a `addons/project/project_phase_estimate/tests/TEST_INSTRUCTIONS.rst`
containing manual instructions. I am asking you to implement this as actual Python
tests.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

### Summary of Changes

All bugs have been identified and fixed in the `project_phase_estimate` module. The
following changes were made:

1. **Fixed `_compute_is_in_progress`** (`models/project_estimate.py`):

   - The compute method incorrectly returned `True` when both `start_date` and
     `end_date` were in the past. Fixed by adding a check that `end_date` is not in the
     past when `start_date` is set and in the past.

2. **Fixed `_compute_estimate_id`** (`models/project_task.py`):

   - Added `("is_in_progress", "=", True)` filter to the estimate search so tasks only
     link to running estimates. The phase domain in the task form
     (`estimate_in_progress_count > 0`) already filtered phases correctly; fixing
     `is_in_progress` resolved the underlying issue.

3. **Fixed cron job `_update_is_in_progress`** (`models/project_estimate.py`):

   - Added `@api.model` decorator and changed the method to search for all estimates
     with `start_date` or `end_date` set, instead of relying on `self` (which was an
     empty recordset when called from cron).

4. **Added archive cascade** (`models/project_project.py`):

   - Overrode `write` on `project.project` to set `active=False` on all related
     estimates when a project is archived.

5. **Added subtask phase inheritance** (`models/project_task.py`):

   - Overrode `create` on `project.task` to propagate `phase_id` from parent to subtask
     when `parent_id` is set and no explicit `phase_id` is provided.

6. **Added project_id domain filter to phase estimates** (`models/project_phase.py`):

   - Updated `action_project_estimate` to append
     `("project_id", "=", default_project_id)` to the domain when `default_project_id`
     is present in context. Also kept `search_default_project_id` in the returned action
     context.

7. **Moved `phase_id` before `user_ids`** (`views/project_task_views.xml`):

   - Restructured the inherited view to replace the original `phase_id` (after
     `project_id`) and reinsert it before `user_ids`, preserving the context and domain
     attributes.

8. **Implemented Python tests** (`tests/test_project_phase_estimate.py`):
   - Created 19 automated tests covering: `is_in_progress` logic (9 scenarios), task
     estimate linking, cron updates, project archive cascade, subtask phase inheritance,
     phase action context/domain, effective hours date filtering, multiple estimates
     splitting, and phase in-progress counts.

### Test Results

All 19 tests pass (0 failures, 0 errors).

---

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
