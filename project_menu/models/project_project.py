# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"
    menu_id = fields.Many2one("ir.ui.menu", string="Generated Menu", ondelete="set null")

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
        action = self.env["ir.actions.act_window"].with_context(lang=lang or self.env.lang)
        action_id = action.search([("name", "=", name)], limit=1)
        vals = {
            "name": name,
            "res_model": "project.task",
            "view_mode": "kanban,tree,form,calendar,pivot,graph,gantt,activity,map",
            "domain": "[('project_id', '=', %s)]" % self.id,
            "context": "{ 'default_project_id': %s, 'search_default_my_tasks': True }" % self.id,
        }
        if not action_id:
            action_id = action.create(vals)
            _logger.info("Created action [%s]: %s (ID: %s)", lang or self.env.lang, name, action_id.id)
        else:
            action_id.write(vals)
            _logger.info("Updated action [%s]: %s (ID: %s)", lang or self.env.lang, name, action_id.id)
        return action_id

    def _create_or_update_menu(self, name, action_id, lang=None):
        """
        Create or update a menu entry for this project.
        Uses the existing menu_id stored on the project record if available.
        """
        menu = self.env["ir.ui.menu"].with_context(lang=lang or self.env.lang)
        menu_id = self.menu_id
        parent_menu_id = self._get_parent_menu_id()
        vals = {
            "name": name,
            "action": "ir.actions.act_window,%s" % action_id.id,
            "parent_id": parent_menu_id,
            "sequence": self.id,
        }
        if not menu_id:
            menu_id = menu.create(vals)
            _logger.info("Created menu [%s]: %s (ID: %s)", lang or self.env.lang, name, menu_id.id)
        else:
            menu_id.write(vals)
            _logger.info("Updated menu [%s]: %s (ID: %s)", lang or self.env.lang, name, menu_id.id)
        return menu_id

    def _get_parent_menu_id(self):
        """
        Determine the parent menu ID based on configuration settings.
        Returns the group stage menu if enabled, otherwise the default projects menu.
        """
        settings = self.env["res.config.settings"].sudo().get_values()
        if settings.get("group_project_stages"):
            return self.env.ref("project.menu_projects_group_stage").id
        return self.env.ref("project.menu_projects").id

    def _remove_menu_and_action(self, lang=None):
        """
        Remove the menu and action associated with this project.
        Uses the stored menu_id to locate the menu and its linked action.
        """
        for project in self:
            name = project._get_menu_name(lang=lang)
            menu = self.env["ir.ui.menu"].with_context(lang=lang or self.env.lang)
            # Use the stored menu_id instead of searching by name
            menu_id = project.menu_id
            if menu_id:
                # Get the action linked to this menu
                action = menu_id.action
                if action:
                    action.unlink()
                    _logger.info("Removed action [%s]: %s", lang or self.env.lang, name)
                menu_id.unlink()
                _logger.info("Removed menu [%s]: %s", lang or self.env.lang, name)

    def _sync_menu_and_action_for_languages(self, langs=None):
        """
        Synchronize menu and action entries across all specified languages.
        Creates or updates entries for each language and stores the first menu as menu_id.
        """
        if langs is None:
            langs = self.env["res.lang"].search([]).mapped("code")
        first_menu = None
        for lang in langs:
            name = self._get_menu_name(lang=lang)
            action = self._create_or_update_action(name, lang=lang)
            menu = self._create_or_update_menu(name, action, lang=lang)
            if first_menu is None:
                first_menu = menu
        self.menu_id = first_menu

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to automatically generate menu and action entries for new projects.
        """
        projects = super().create(vals_list)
        for project in projects:
            project._sync_menu_and_action_for_languages()
        return projects

    def write(self, vals):
        """
        Override write to update or remove menu/action when name, key, or active changes.
        """
        if "name" in vals or "key" in vals or "active" in vals:
            for project in self:
                if project.active and ("name" in vals or "key" in vals):
                    project._sync_menu_and_action_for_languages()
                elif not project.active and "active" in vals:
                    project._remove_menu_and_action()
                    project.menu_id = False
        return super().write(vals)

    def toggle_active(self):
        """
        Override toggle_active to handle menu/action cleanup or recreation on activation.
        """
        res = super().toggle_active()
        for project in self:
            if not project.active:
                project._remove_menu_and_action()
                project.menu_id = False
            else:
                project._sync_menu_and_action_for_languages()
        return res
