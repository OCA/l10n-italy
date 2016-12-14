# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'
    non_taxable_nature = fields.Selection([
        ('N1', 'escluse ex art. 15'),
        ('N2', 'non soggette'),
        ('N3', 'non imponibili'),
        ('N4', 'esenti'),
        ('N5', 'regime del margine'),
        ('N6', 'inversione contabile (reverse charge)'),
        ('N7', 'IVA assolta in altro stato UE'),
        ], string="Non taxable nature",
        help="N7: (vendite a distanza ex art. 40 c. 3 e 4 e art. 41 c. 1 lett."
             "b, DL 331/93; prestazione di servizi di telecomunicazioni, "
             "tele-radiodiffusione ed elettronici ex art. 7-sexies lett. f, g,"
             "art. 74-sexies DPR 633/72)"
    )
    payability = fields.Selection([
        ('I', 'Immediate payability'),
        ('D', 'Deferred payability'),
        ('S', 'Split payment'),
        ], string="VAT payability")
    law_reference = fields.Char(
        'Law reference', size=128)
