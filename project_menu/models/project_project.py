# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"

    menu_id = fields.Many2one("ir.ui.menu", string="Generated Menu", ondelete="set null", copy=False)
    action_id = fields.Many2one("ir.actions.act_window", string="Generated Action", ondelete="set null", copy=False)

    def _get_menu_name(self, lang=None):
        """
        Generate the menu name for this project, optionally localized.
        Includes project name and key if available.
        """
        self.ensure_one()
        name = _("Project tasks") + " " + self.name
        if self.key:
            name += " (" + self.key + ")"
        return name

    def _create_or_update_action(self, name, lang=None):
        """
        Create or update an action for viewing tasks of this project.
        The action is localized per language and linked to project tasks.
        """
        action_model = self.env["ir.actions.act_window"].with_context(lang=lang or self.env.lang)
        vals = {
            "name": name,
            "res_model": "project.task",
            "view_mode": "kanban,list,form,calendar,pivot,graph,gantt,activity,map",
            "domain": "[('project_id', '=', %s)]" % self.id,
            "context": "{ 'default_project_id': %s, 'search_default_my_tasks': True }" % self.id,
        }
        if not self.action_id:
            action_id = action_model.create(vals)
            self.action_id = action_id
        else:
            self.action_id.with_context(lang=lang or self.env.lang).write(vals)
        return self.action_id

    def _create_or_update_menu(self, name, action_id, lang=None):
        """
        Create or update a menu entry for this project.
        Uses the existing menu_id stored on the project record if available.
        """
        menu_model = self.env["ir.ui.menu"].with_context(lang=lang or self.env.lang)
        vals = {
            "name": name,
            "action": "ir.actions.act_window,%s" % action_id.id,
            "parent_id": self._get_parent_menu_id(),
            "sequence": self.id,
        }
        if not self.menu_id:
            menu_id = menu_model.create(vals)
            self.menu_id = menu_id
        else:
            self.menu_id.with_context(lang=lang or self.env.lang).write(vals)
        return self.menu_id

    def _get_parent_menu_id(self):
        """
        Determine the parent menu ID based on configuration settings.
        Returns the group stage menu if enabled, otherwise the default projects menu.
        """
        if self.env.user.has_group("project.group_project_stages"):
            return self.env.ref("project.menu_projects_group_stage").id
        return self.env.ref("project.menu_projects").id

    def _remove_menu_and_action(self, lang=None):
        """
        Remove the menu and action associated with this project.
        Uses the stored menu_id and action_id to locate and unlink them.
        """
        for project in self:
            if project.menu_id:
                menu_name = project._get_menu_name(lang=lang)
                project.menu_id.unlink()
                project.menu_id = False
            if project.action_id:
                action_name = project._get_menu_name(lang=lang)
                project.action_id.unlink()
                project.action_id = False

    def _sync_menu_and_action_for_languages(self, lang_codes=None):
        """
        Synchronize menu and action entries across all specified languages.
        Creates or updates entries for each language.
        """
        lang_codes = lang_codes or self.env["res.lang"].search([]).mapped("code")
        for lang_code in lang_codes:
            name = self._get_menu_name(lang=lang_code)
            action_id = self._create_or_update_action(name, lang=lang_code)
            menu_id = self._create_or_update_menu(name, action_id, lang=lang_code)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Extend create to automatically generate menu and action entries for new projects.
        """
        projects = super().create(vals_list)
        for project in projects:
            project._sync_menu_and_action_for_languages()
        return projects

    def write(self, vals):
        """
        Extend write to update or remove menu/action when name, key, or active changes.
        """
        res = super().write(vals)
        if "name" in vals or "key" in vals or "active" in vals:
            for project in self:
                if project.active and ("name" in vals or "key" in vals):
                    project._sync_menu_and_action_for_languages()
                elif not project.active and "active" in vals:
                    project._remove_menu_and_action()
        return res

    def toggle_active(self):
        """
        Extend toggle_active to handle menu/action cleanup or recreation on activation.
        """
        res = super().toggle_active()
        for project in self:
            if not project.active:
                project._remove_menu_and_action()
            else:
                project._sync_menu_and_action_for_languages()
        return res
