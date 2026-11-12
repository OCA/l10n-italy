# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import _, models


class ShippingInformationUpdaterMixin(models.AbstractModel):
    _name = "shipping.information.updater.mixin"
    _description = "Shipping Information Updater Mixin"

    def _update_generic_shipping_information(self, record):
        """Copy the defaults of `record` on self.

        Return the labels of the fields that already had a different value
        and have been overwritten (empty list if none).
        """
        changed = []
        for field in (
            "transport_condition_id",
            "goods_appearance_id",
            "transport_reason_id",
            "transport_method_id",
        ):
            default = record["default_" + field]
            if default and self[field] != default:
                if self[field]:
                    changed.append(self._fields[field]._description_string(self.env))
                self[field] = default
        return changed

    def _get_shipping_overwritten_warning(self, changed, origin):
        return {
            "warning": {
                "title": _("Warning!"),
                "message": _(
                    "The following shipping configuration have been overwritten "
                    "with the default ones of the selected %(origin)s: "
                    "%(fields)s.\n"
                    "Please, make sure to check this information before "
                    "continuing.",
                    origin=origin,
                    fields=", ".join(changed),
                ),
            }
        }

    def _update_partner_shipping_information(self, partner):
        changed = []

        if (
            partner.property_delivery_carrier_id
            and self.delivery_method_id != partner.property_delivery_carrier_id
        ):
            if self.delivery_method_id:
                changed.append(
                    self._fields["delivery_method_id"]._description_string(self.env)
                )

            self.delivery_method_id = partner.property_delivery_carrier_id

        changed += self._update_generic_shipping_information(partner)

        return changed
