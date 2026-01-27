# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Menu",
    "summary": """
        Add each project as menu entry.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project_key"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "post_init_hook": "_install_project_menu",
    "uninstall_hook": "_uninstall_project_menu",
}
