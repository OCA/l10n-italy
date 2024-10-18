# Copyright (c) 2023, Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    display_ref_order_dn_report = fields.Boolean(
        "Display Ref. Order in Delivery Note Report",
        default=False,
    )
    display_ref_customer_dn_report = fields.Boolean(
        "Display Ref. Customer in Delivery Note Report",
        default=False,
    )
    display_carrier_dn_report = fields.Boolean(
        "Display Carrier in Delivery Note Report",
        default=False,
    )
    display_delivery_method_dn_report = fields.Boolean(
        "Display Delivery Method in Delivery Note Report",
        default=False,
    )

    @api.model_create_multi
    def create(self, vals):
        """
        Create DN types and their sequences after companies creation
        if they're not already existing
        """
        res = super().create(vals)
        for company in res:
            self.env["stock.delivery.note.type"].sudo().create_dn_types(company)
        return res
