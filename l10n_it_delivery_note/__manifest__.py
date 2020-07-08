# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    'name': "ITA - Documento di Trasporto",
    'summary': "Crea, gestisci e fattura i DdT partendo dalle Consegne",

    'author': "Marco Calcagni, Gianmarco Conte, Link IT Europe Srl, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/tree/12.0/'
               'l10n_it_delivery_note',
    'version': '12.0.1.0.0',
    'category': "Localization",
    'license': 'AGPL-3',

    'depends': [
        'delivery',
        'l10n_it_delivery_note_base',
        'mail',
        'sale_stock',
        'stock_account'
    ],

    'data': [
        'report/report_delivery_note.xml',

        'security/ir.model.access.csv',
        'security/ir_module_category.xml',
        'security/ir_rule.xml',
        'security/res_groups.xml',
        'security/res_users.xml',

        'views/account_invoice.xml',
        'views/assets.xml',
        'views/res_config_settings.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/stock_delivery_note.xml',
        'views/stock_picking.xml',

        'wizard/delivery_note_create.xml',
        'wizard/delivery_note_select.xml',
        'wizard/delivery_note_template.xml'
    ]
}
