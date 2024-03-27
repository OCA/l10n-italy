# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockDeliveryNote(models.Model):
    _name = "stock.delivery.note"
    _inherit = ["stock.delivery.note", "comment.template"]
