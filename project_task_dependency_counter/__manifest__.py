{
    'name': "Project Task Dependency Counter",

    'summary': """
        Module summary.
    """,
    
    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': 'https://www.mint-system.ch',
    'category': 'Project',
    'version': '13.0.1.0.0',
    'license': 'AGPL-3',
    
    'depends': ['project_task_dependency'],

    'data': [
        'views/project_task_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}