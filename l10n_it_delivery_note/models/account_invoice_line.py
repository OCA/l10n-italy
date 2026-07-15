# Copyright 2022 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    delivery_note_id = fields.Many2one(
        comodel_name="stock.delivery.note",
        string="Delivery Note",
        compute="_compute_delivery_note_id",
        readonly=False,
        store=True,
        copy=False,
    )
    delivery_note_line_id = fields.Many2one(
        comodel_name="stock.delivery.note.line",
        string="Delivery Note Line",
        readonly=True,
        copy=False,
    )
    note_dn = fields.Boolean(string="Note DN")

    @api.depends(
        "delivery_note_line_id",
    )
    def _compute_delivery_note_id(self):
        for line in self:
            line.delivery_note_id = line.delivery_note_line_id.delivery_note_id
