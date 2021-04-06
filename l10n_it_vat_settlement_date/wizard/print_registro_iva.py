# Copyright (c) 2021 Marco Colombo <https://github/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    def _get_move_ids(self, wizard):
        moves = self.env['account.move'].search([
            '|', '&', ('date_vat_settlement', '>=', self.from_date), ('date_vat_settlement', '<=', self.to_date),
                 '&', ('date_vat_settlement', '=', None), '&', ('date', '<=', self.to_date), ('date', '>=', self.from_date),
            ('journal_id', 'in', [j.id for j in self.journal_ids]),
            ('state', '=', 'posted'), ], order='date, name')
        return moves.ids
