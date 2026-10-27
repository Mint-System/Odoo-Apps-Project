# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Update List",
    "summary": """
        Prepare multiple project updates from kanban phase or list view.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Project",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_update_views.xml",
        "views/project_project_views.xml",
        "wizard/prepare_project_update_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
