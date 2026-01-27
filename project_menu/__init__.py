from . import models

from odoo import api, SUPERUSER_ID


def _install_project_menu(cr, registry):
    """
    Hook to create menu and action entries for all existing projects on install.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    for project in env["project.project"].search([]):
        if project.active:
            project._sync_menu_and_action_for_languages()


def _uninstall_project_menu(cr, registry):
    """
    Hook to remove all generated menus and actions on uninstall.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    for project in env["project.project"].search([]):
        project._remove_menu_and_action()
        project.write({"menu_id": False})
