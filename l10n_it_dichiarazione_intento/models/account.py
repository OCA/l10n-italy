# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountFiscalPosition(models.Model):

    _inherit = 'account.fiscal.position'

    valid_for_dichiarazione_intento = fields.Boolean(
        "Valid for declaration of intent")

    @api.constrains('valid_for_dichiarazione_intento', 'tax_ids')
    @api.multi
    def _check_taxes_for_dichiarazione_intento(self):
        for fiscal_position in self:
            if fiscal_position.valid_for_dichiarazione_intento and \
                    not fiscal_position.tax_ids:
                raise ValidationError(_(
                    'Define taxes for fiscal position %s valid '
                    'for declaration of intent') % fiscal_position.name)


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    force_dichiarazione_intento_id = fields.Many2one(
        'dichiarazione.intento',
        string='Force Declaration of Intent')
