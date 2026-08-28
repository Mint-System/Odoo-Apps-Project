# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Project Task",
    "summary": """
        Link helpdesk tickets to project tasks.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Helpdesk",
    "version": "18.0.1.0.0",
    "license": "OPL-1",
    "depends": ["helpdesk_timesheet"],
    "data": [
        "views/helpdesk_ticket_views.xml",
        "views/project_task_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
