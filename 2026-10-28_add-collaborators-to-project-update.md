---
commit_ref: 6d24f74cf97d3f070af808f1f719ee551b3ab8e7
title: "Add collaborators to project update"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-28
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 87680
output_tokens: 15983
---

# Add collaborators to project update

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

Update the module `addons/project/project_update_list`

The`action_open_form` must show the list of updates of the linked project and not the
form of this update.

Make `project.collaborator_ids` on project form editable.

Link `project.update:collaborator_ids` with `project_id.collaborator_ids`.

Show collaborator names as badge on project update list.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

- Fixed `action_open_form` on `project.update` to return a tree view action filtered by
  `project_id` instead of opening the single update form.
- Added `collaborator_ids` Many2many field on `project.update`, related to
  `project_id.collaborator_ids.partner_id`.
- Added `collaborator_ids` to the project update list view tree with `many2many_tags`
  widget (optional, shown by default).
- Inherited `project.collaborator` to make `partner_id` writable so new collaborators
  can be added inline.
- Added inherited view on `project.project` form to display `collaborator_ids` as an
  inline editable tree after the Project Manager field.
- Updated German translation for the new "Collaborators" field string.
- Added tests for `action_open_form` list behavior and `collaborator_ids` related field.
- Note: Database was not running; tests were not executed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
