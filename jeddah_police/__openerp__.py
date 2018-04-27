# -*- coding: utf-8 -*-
{
    'name': "Full Police Cases Detail",

    'summary': "Full Police Cases Detail",

    'description': "Full Police Cases Detail",

    'author': "Ecube",
    'website': "http://www.ecube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','police_project'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
