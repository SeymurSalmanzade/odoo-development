# -*- coding: utf-8 -*-
{
    'name': "book_store",

    'summary': "selling books and movies",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/genre_view.xml',
        'views/category_view.xml',
        'views/book_store_view.xml',
        'views/movie_store_view.xml',
        'views/res_currency.xml',
        'templates/book_template.xml',
        'templates/movie_template.xml',
        'templates/inherit_book_template.xml',
        'views/mb_sellers_view.xml',
        'views/mb_companies_view.xml',
        'data/ir_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True
}

