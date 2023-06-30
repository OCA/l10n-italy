# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockDeliveryNote(models.Model):
    _name = "stock.delivery.note"
    _inherit = ["stock.delivery.note", "comment.template"]
