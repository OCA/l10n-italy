# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    prod_lot_ids = fields.Many2many(
        comodel_name="stock.production.lot",
        compute="_compute_prod_lots",
        string="Production Lots",
    )

    @api.depends("move_line_ids")
    def _compute_prod_lots(self):
        for line in self:
            line.prod_lot_ids = line.mapped("move_line_ids.move_line_ids.lot_id")

    def lots_grouped_by_quantity(self):
        lot_dict = defaultdict(float)
        for sml in self.mapped("move_line_ids.move_line_ids"):
            lot_dict[sml.lot_id.name] += sml.qty_done
        return lot_dict
