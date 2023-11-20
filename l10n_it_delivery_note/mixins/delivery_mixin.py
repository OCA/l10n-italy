#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


def _default_volume_uom(model):
    return model.env.ref("uom.product_uom_litre", raise_if_not_found=False)


def _domain_volume_uom(model):
    uom_category_id = model.env.ref(
        "uom.product_uom_categ_vol", raise_if_not_found=False
    )

    return [("category_id", "=", uom_category_id.id)]


def _default_weight_uom(model):
    return model.env.ref("uom.product_uom_kgm", raise_if_not_found=False)


def _domain_weight_uom(model):
    uom_category_id = model.env.ref(
        "uom.product_uom_categ_kgm", raise_if_not_found=False
    )

    return [("category_id", "=", uom_category_id.id)]


class DeliveryData(models.AbstractModel):
    _name = "l10n_it_delivery_note.delivery_mixin"
    _description = "Common data for records to be delivered"

    delivery_transport_reason_id = fields.Many2one(
        comodel_name="stock.picking.transport.reason",
        string="Reason of transport of Delivery",
    )
    delivery_transport_condition_id = fields.Many2one(
        comodel_name="stock.picking.transport.condition",
        string="Condition of transport of Delivery",
    )
    delivery_transport_method_id = fields.Many2one(
        comodel_name="stock.picking.transport.method",
        string="Method of transport of Delivery",
    )
    delivery_carrier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Carrier of Delivery",
    )
    delivery_goods_appearance_id = fields.Many2one(
        comodel_name="stock.picking.goods.appearance",
        string="Appearance of goods of Delivery",
    )
    delivery_volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume of Delivery UoM",
        default=_default_volume_uom,
        domain=_domain_volume_uom,
    )
    delivery_volume = fields.Float(
        string="Volume of Delivery",
    )
    delivery_gross_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Gross Weight of Delivery UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
    )
    delivery_gross_weight = fields.Float(
        string="Gross Weight of Delivery",
    )
    delivery_net_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Net Weight of Delivery UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
    )
    delivery_net_weight = fields.Float(
        string="Net Weight of Delivery",
    )
    delivery_transport_datetime = fields.Datetime(
        string="Transport Date of Delivery",
    )
    delivery_packages = fields.Integer(
        string="Packages of Delivery",
    )
    delivery_note = fields.Html(
        string="Internal note of delivery",
    )
