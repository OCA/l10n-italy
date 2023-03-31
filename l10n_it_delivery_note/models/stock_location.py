# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.model
    def get_virtual_locations_root(self):
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        location_id = IrConfigParameter.get_param("stock.location.virtual_root")
        if location_id:
            virtual_locations_root = self.browse(int(location_id)).exists()

        else:
            ResConfigSettings = self.env["res.config.settings"].sudo()
            virtual_locations_root = ResConfigSettings._default_virtual_locations_root()

            if virtual_locations_root:
                IrConfigParameter.set_param(
                    "stock.location.virtual_root", virtual_locations_root.id
                )

        if not virtual_locations_root:
            raise UserError(
                _(
                    "Can't find a default virtual locations root.\n"
                    "Ask your system administrator"
                    " to set it from the Warehouse"
                    " configurations page before continue."
                )
            )

        return virtual_locations_root

    def is_virtual(self):
        virtual_locations_root = self.get_virtual_locations_root()

        return self.parent_path.startswith(virtual_locations_root.parent_path)
