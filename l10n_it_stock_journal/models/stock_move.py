# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def _selection_move_journal_type(self):
        return [
            ('internal', 'Internal'),
            ('incoming', 'Incoming'),
            ('outcoming', 'Outcoming'),
        ]

    move_journal_type = fields.Selection(
        selection='_selection_move_journal_type',
        compute='_compute_move_journal_type', store=True, readonly=True)

    @api.multi
    @api.depends('location_id', 'location_dest_id')
    def _compute_move_journal_type(self):
        for move in self:
            if (
                    move.location_id.usage == 'internal'
                    and move.location_dest_id.usage == 'internal'
            ):
                move.move_journal_type = 'internal'
            elif (
                    move.location_id.usage == 'internal'
                    and move.location_dest_id.usage != 'internal'
            ):
                move.move_journal_type = 'outcoming'
            elif (
                    move.location_id.usage != 'internal'
                    and move.location_dest_id.usage == 'internal'
            ):
                move.move_journal_type = 'incoming'


