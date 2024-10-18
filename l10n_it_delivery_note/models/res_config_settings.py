# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _default_virtual_locations_root(self):
        return self.env.ref(
            "stock.stock_location_locations_virtual", raise_if_not_found=False
        )

    group_required_partner_ref = fields.Boolean(
        string="Make Partner Ref. in DN Mandatory",
        implied_group="l10n_it_delivery_note.group_required_partner_ref",
    )

    virtual_locations_root = fields.Many2one(
        "stock.location",
        string="Virtual locations root",
        default=_default_virtual_locations_root,
        config_parameter="stock.location.virtual_root",
    )

    display_ref_order_dn_report = fields.Boolean(
        string="Display Ref. Order in Delivery Note Report",
        related="company_id.display_ref_order_dn_report",
        readonly=False,
    )
    display_ref_customer_dn_report = fields.Boolean(
        string="Display Ref. Customer in Delivery Note Report",
        related="company_id.display_ref_customer_dn_report",
        readonly=False,
    )
    display_carrier_dn_report = fields.Boolean(
        string="Display Carrier in Delivery Note Report",
        related="company_id.display_carrier_dn_report",
        readonly=False,
    )
    display_delivery_method_dn_report = fields.Boolean(
        string="Display Delivery Method in Delivery Note Report",
        related="company_id.display_delivery_method_dn_report",
        readonly=False,
    )
