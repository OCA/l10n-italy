from odoo import fields, models


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
