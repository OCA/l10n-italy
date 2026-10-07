# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = "res.config.settings"

    sepa_payment_order_schema = fields.Selection(
        related="company_id.sepa_payment_order_schema",
        readonly=False,
    )
