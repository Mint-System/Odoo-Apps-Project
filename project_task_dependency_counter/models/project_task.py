from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    dependency_task_ids_count = fields.Integer(
        string="Dependency Tasks Count", compute="_compute_dependency_task_ids_count"
    )

    def _compute_dependency_task_ids_count(self):
        for task in self:
            task.dependency_task_ids_count = len(task.get_dependency_tasks())

    def view_dependency_task_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Dependencies",
            "view_mode": "kanban,form",
            "res_model": "project.task",
            "domain": [("id", "in", [t.id for t in self.dependency_task_ids])],
        }
