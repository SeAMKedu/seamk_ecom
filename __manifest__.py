# -*- coding: utf-8 -*-
{
    'name': "seamk_ecom",
    'summary': """Add FEA calculation to the online shop.""",
    'description': """
        If the shopping cart contains a product called 'Support', the module
        extends the default checkout process by adding an extra page for a
        customer to set the input parameters of the support: the distances of
        the 3 holes and a force (weight) that is affecting to the support.
        These input parameters are sent to the REST API of the external MES
        application. After a FEA (Finite Element Analysis) is done, the API 
        returns the following parameters: R1, R2, area, and stress. Both
        inputs and results of the FEA are stored to the field 'x_fea_params'
        of the sale order record.
    """,
    'author': "SeAMK",
    'website': "https://www.seamk.fi/en/",
    'category': 'Website',
    'version': '0.1',
    'depends': ['website_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    # (Added) Custom JS files.
    'js': [
        'static/js/fea.js'
    ],
    # (Added) How the module is installed.
    'installable': True,
    'auto_install': False
}
