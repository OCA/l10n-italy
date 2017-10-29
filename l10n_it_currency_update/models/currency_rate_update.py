# -*- coding: utf-8 -*-
# Copyright 2017 Giacomo Grasso, Gabriele Baldessari
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class CurrencyRateUpdateService(models.Model):
    """ Inheritin the class in order to add the
        Bank of Italy to the selection field
    """
    _inherit = "currency.rate.update.service"
    _description = "Currency Rate Update"

    service = fields.Selection(selectoin_add=[('italy', 'Bank of Italy')])
