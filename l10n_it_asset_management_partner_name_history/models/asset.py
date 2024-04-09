#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Asset(models.Model):
    _inherit = "asset.asset"
    _partner_name_history_field_map = {
        "customer_id": "sale_date",
        "supplier_id": "purchase_date",
    }
