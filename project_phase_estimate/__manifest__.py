{
    "name": "Project Phase Estimate",
    "summary": """
        Estimate planned hours by project and phases.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "15.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["project_phase", "hr_timesheet"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_estimate.xml",
        "views/project_project.xml",
        "views/project_task.xml",
        "views/project_phase.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
