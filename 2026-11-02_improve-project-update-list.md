---
commit_ref: cf0d0ebdf02d4fb6de8b49eb19f182424605f398
title: "Improve Project Update List"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-11-02
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 31904
output_tokens: 7315
---

# Improve Project Update List

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

Imporovments for `project_update_list` module.

The default sort for `project.update` is:

1. project_id
2. project_user_id
3. date

So when I check the list I see the latest updates by project manager and project.

Then I want you to update the `name` filter. The field-filter should also search
`project_id`. Then add `partner_id` as new filed to filter.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

- Updated `_order` on `project.update` from `batch, project_user_id, date desc` to
  `project_id, project_user_id, date desc` in `models/project_update.py`.
- Added `filter_domain` to the `name` search field so it also matches `project_id` in
  the inherited search view.
- Added `partner_id` as a new searchable field in the search view.
- Pre-commit linting passed for the module.

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
