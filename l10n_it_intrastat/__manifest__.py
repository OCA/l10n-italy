
{
    'name': 'ITA - Intrastat',
    'version': '11.0.1.0.0',
    'category': 'Account',
    'summary': 'Riclassificazione merci e servizi per dichiarazioni Intrastat',
    'author': 'Openforce'
              ', Link IT srl, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    "depends": [
        'sale_management',
        'product',
        'stock',
        'stock_account',
        'report_intrastat'],
    "data": [
        'security/ir.model.access.csv',
        'views/intrastat.xml',
        'views/product.xml',
        'views/account.xml',
        'views/config.xml',
        'data/account.intrastat.transation.nature.csv',
        'data/account.intrastat.transport.csv',
        'data/account.intrastat.custom.csv',
        'data/report.intrastat.code.csv',
    ],
    "demo": [
        'demo/product_demo.xml'
    ],
    "installable": True
}
