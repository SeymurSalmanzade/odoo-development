# -*- coding: utf-8 -*-
{
    'name': "task_template",

    'summary': "template for task",

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
    'depends': ['base','account_accountant','contacts','sale_management','crm','web_studio','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates/invoice_document_report_inherit.xml',
        'templates/boxed_layout_inherit.xml',
        'templates/web_address_layout_inherit.xml',
        'templates/tax_groups_totals_inherit.xml',
        'templates/tax_totals_inherit.xml',
        'views/res_bank_view.xml',
        'reports/report_invoice_az.xml',
        'templates/web_external_layout_inherit.xml',
        'templates/report_purchaseorder_document.xml',
        'views/purchase_order_view.xml',
        'views/res_company_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    # 'application': False,
    # 'auto_install': False,
}