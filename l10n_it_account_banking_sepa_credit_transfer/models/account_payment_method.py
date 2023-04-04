# Copyright 2016-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    pain_version = fields.Selection(
        selection_add=[
            ("pain.00.04.00", "pain.00.04.00 (credit transfer in Italy)"),
        ],
        ondelete={
            "pain.00.04.00": "set null",
        },
    )
