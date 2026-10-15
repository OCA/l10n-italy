from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    use_dn_product_name_in_invoice = fields.Boolean(
        string="Use Delivery Note Product Name in Invoice",
        default=False,
    )
    use_dn_price_unit_in_invoice = fields.Boolean(
        string="Use Delivery Note Price Unit in Invoice",
        default=False,
    )

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
