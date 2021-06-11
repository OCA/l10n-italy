# Copyright 2022 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    delivery_note_id = fields.Many2one(
        "stock.delivery.note", string="Delivery Note", readonly=True, copy=False
    )
    note_dn = fields.Boolean(string="Note DN")
