# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2020 Simone Vanin - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models

from odoo.addons.l10n_it_delivery_note.mixins.delivery_mixin import (
    _default_volume_uom,
    _default_weight_uom,
)


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "l10n_it_delivery_note.delivery_mixin",
    ]

    def _default_volume_uom(self):
        return _default_volume_uom(self)

    def _default_weight_uom(self):
        return _default_weight_uom(self)

    @api.onchange(
        "partner_id",
    )
    def _onchange_partner_shipping_data(self):
        for invoice in self:
            partner = invoice.partner_id
            if partner:
                invoice.delivery_transport_reason_id = (
                    partner.default_transport_reason_id
                )
                invoice.delivery_transport_condition_id = (
                    partner.default_transport_condition_id
                )
                invoice.delivery_transport_method_id = (
                    partner.default_transport_method_id
                )
                invoice.delivery_goods_appearance_id = (
                    partner.default_goods_appearance_id
                )
