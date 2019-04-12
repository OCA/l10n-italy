# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2015 Alessio Gerace <alessio.gerace@agilebg.com>
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - Registro REA',
    'version': '10.0.1.1.2',
    'category': 'Localisation/Italy',
    'summary': 'Gestisce i campi del Repertorio Economico Amministrativo',
    'author': 'Agile Business Group, Odoo Italia Network,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/l10n_it_rea',
    'license': 'AGPL-3',
    "depends": [
        'account'
    ],
    "data": [
        'views/partner_view.xml',
        'views/company_view.xml',
    ],
    'installable': True,
}
