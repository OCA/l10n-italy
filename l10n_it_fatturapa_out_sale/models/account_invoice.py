# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_sale_order_data = fields.Boolean(
        related='partner_id.fatturapa_sale_order_data'
    )
