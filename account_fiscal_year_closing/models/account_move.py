# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _selection_closing_type(self):
        """Use selection values from move_type field in closing config
        (making a copy for preventing side effects), plus an extra value for
        non-closing moves."""
        res = list(
            self.env['account.fiscalyear.closing.config'].fields_get(
                allfields=['move_type']
            )['move_type']['selection']
        )
        res.append(('none', _('None')))
        return res

    fyc_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing', delete="cascade",
        string="Fiscal year closing", readonly=True,
    )
    closing_type = fields.Selection(
        selection=_selection_closing_type, default="none",
        states={'posted': [('readonly', True)]},
    )
