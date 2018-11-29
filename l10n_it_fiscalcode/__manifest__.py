# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2018 Matteo Bilotta (Link IT s.r.l.)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2018 Teuron (<http://www.teuron.it>)
# Copyright 2018 RDS S.p.A. (<http://www.rdsmoulding.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localisation - Fiscal Code',
    'version': '12.0.2.0.0',
    'category': 'Localisation/Italy',
    'author': "Link IT s.r.l., "
              "Teuron SRL, "
              "RDS Moulding Technology SpA, "
              "Apulia Software, "
              "Odoo Italia Network, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': ['base_vat'],
    'data': [
        'view/fiscalcode_view.xml'
        ],
    'images': [],
    'installable': True
}