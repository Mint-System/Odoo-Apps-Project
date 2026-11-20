# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Cost Cockpit",
    "summary": """
        Report project costs from analytic lines.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Project",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "project",
        "hr_timesheet",
        "mrp_account",
        "project_mrp_account",
        "sale_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/project_cost_report_views.xml",
        "report/project_report_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_cost_cockpit/static/src/js/project_report_pivot.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
