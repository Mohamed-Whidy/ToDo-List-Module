{
    'name': "To-Do List Module",
    'version': '1.0',
    'author': "Whidy96",
    'category': '',
    'summary': """Task List Management""",
    'description': """Management Tasks""",

    # data files always loaded at installation
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_task_root_menu.xml',
        'views/todo_task_view.xml',
    ],
    'assets': {
            'web.assets_backend': ['todo_management/static/src/css/todo_task.css']
        },
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': True
}
