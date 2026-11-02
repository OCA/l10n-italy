# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    sepa_payment_order_schema = fields.Selection(
        [
            ("CORE", "Basic (CORE)"),
            ("B2B", "Enterprise (B2B)"),
        ],
        string="Payment Order Scheme",
        default="CORE",
    )
