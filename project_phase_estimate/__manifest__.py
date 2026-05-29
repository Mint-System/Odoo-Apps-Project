{
    "name": "Project Phase Estimate",
    "summary": """
        Estimate planned hours by project and phases.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Tools",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project_phase", "sale_timesheet"],
    "data": [
        "data/ir_cron_data.xml",
        "security/ir.model.access.csv",
        "views/project_estimate_views.xml",
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/project_phase_views.xml",
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
