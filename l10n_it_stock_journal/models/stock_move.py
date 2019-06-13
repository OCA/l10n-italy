# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def _selection_usage(self):
        return [
            ('internal', 'Internal'),
            ('loading', 'Loading'),
            ('unloading', 'Unloading'),
        ]

    usage = fields.Selection(
        selection='_selection_usage',
        compute='_compute_usage', store=True, readonly=True)

    @api.multi
    @api.depends('location_id', 'location_dest_id')
    def _compute_usage(self):
        for move in self:
            if (
                    move.location_id.usage == 'internal'
                    and move.location_dest_id.usage == 'internal'
            ):
                move.usage = 'internal'
            elif (
                    move.location_id.usage == 'internal'
                    and move.location_dest_id.usage != 'internal'
            ):
                move.usage = 'unloading'
            elif (
                    move.location_id.usage != 'internal'
                    and move.location_dest_id.usage == 'internal'
            ):
                move.usage = 'loading'


