##############################################################################
#
#    Copyright (C) 2013-2017 Agile Business Group sagl (http://www.agilebg.com)
#    @author Alex Comba <alex.comba@agilebg.com>
#    @author Lorenzo Battistini <https://github.com/eLBati>
#    Copyright (C) 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
#    @author Diego Bruselli <d.bruselli@creativiquadrati.it>
#    Copyright (C) 2013
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

{
    'name': 'ITA - Bolle doganali',
    'version': '12.0.1.0.0',
    'category': 'Localization/Italy',
    'author': "Agile Business Group, CQ Creativi Quadrati, TAKOBI, "
              "Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_bill_of_entry",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/company_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
        'demo/bill_of_entry_demo.xml',
    ],
    'installable': True,
}
