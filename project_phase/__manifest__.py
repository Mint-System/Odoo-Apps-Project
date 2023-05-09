{
    "name": "Project Phase",
    "summary": """
        Manage project task by project phases.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": ["security/ir.model.access.csv", "views/project_view.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
