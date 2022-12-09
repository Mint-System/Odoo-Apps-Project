{
    "name": "Project Key Link Type",
    "summary": """
        Create project key from type sequence.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Project",
    "version": "15.0.1.3.2",
    "license": "AGPL-3",
    "depends": ["project_type", "project_template"],
    "data": [
        "data/project_sequence.xml",
        "views/project_task.xml",
        "views/project_project.xml",
        "views/project_type.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
