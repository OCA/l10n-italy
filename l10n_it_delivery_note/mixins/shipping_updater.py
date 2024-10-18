# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import models


class ShippingInformationUpdaterMixin(models.AbstractModel):
    _name = "shipping.information.updater.mixin"
    _description = "Shipping Information Updater Mixin"

    def _update_generic_shipping_information(self, record):
        changed = False

        if (
            record.default_transport_condition_id
            and self.transport_condition_id != record.default_transport_condition_id
        ):
            if self.transport_condition_id:
                changed = True

            self.transport_condition_id = record.default_transport_condition_id

        if (
            record.default_goods_appearance_id
            and self.goods_appearance_id != record.default_goods_appearance_id
        ):
            if self.goods_appearance_id:
                changed = True

            self.goods_appearance_id = record.default_goods_appearance_id

        if (
            record.default_transport_reason_id
            and self.transport_reason_id != record.default_transport_reason_id
        ):
            if self.transport_reason_id:
                changed = True

            self.transport_reason_id = record.default_transport_reason_id

        if (
            record.default_transport_method_id
            and self.transport_method_id != record.default_transport_method_id
        ):
            if self.transport_method_id:
                changed = True

            self.transport_method_id = record.default_transport_method_id

        return changed

    def _update_partner_shipping_information(self, partner):
        changed = False

        if (
            partner.property_delivery_carrier_id
            and self.delivery_method_id != partner.property_delivery_carrier_id
        ):
            if self.delivery_method_id:
                changed = True

            self.delivery_method_id = partner.property_delivery_carrier_id

        changed |= self._update_generic_shipping_information(partner)

        return changed
