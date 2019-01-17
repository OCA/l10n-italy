# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Gianmarco Conte - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class FatturapaPaymentMethod(models.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment_method"
    _description = 'Fiscal Payment Method'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)

