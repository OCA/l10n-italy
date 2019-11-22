# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create_from_ui(self, partner):
        if 'electronic_invoice_subjected' in partner:
            partner['electronic_invoice_subjected'] = \
                partner['electronic_invoice_subjected'] == 'true'
        return super(ResPartner, self).create_from_ui(partner)
