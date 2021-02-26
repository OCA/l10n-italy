# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _default_virtual_locations_root(self):
        return self.env.ref(
            "stock.stock_location_locations_virtual", raise_if_not_found=False
        )

    group_use_advanced_delivery_notes = fields.Boolean(
        string="Use Advanced DN Features",
        implied_group="l10n_it_delivery_note.use_advanced_delivery_notes",
    )

    virtual_locations_root = fields.Many2one(
        "stock.location",
        string="Virtual locations root",
        default=_default_virtual_locations_root,
        config_parameter="stock.location.virtual_root",
    )
