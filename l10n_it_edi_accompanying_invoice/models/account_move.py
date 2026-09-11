# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

from odoo.addons.l10n_it_delivery_note.mixins.delivery_mixin import _default_weight_uom


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_it_edi_accompanying_get_weights(self):
        """Compute the weights and UoMs to include in the e-invoice."""
        self.ensure_one()
        weights_vals = {}
        gross_weight, net_weight = self.delivery_gross_weight, self.delivery_net_weight
        if not (gross_weight or net_weight):
            return weights_vals

        default_uom = (
            _default_weight_uom(self)
            or self.env[
                "product.template"
            ]._get_weight_uom_id_from_ir_config_parameter()
        )
        gross_weight_uom, net_weight_uom = (
            self.delivery_gross_weight_uom_id or default_uom,
            self.delivery_net_weight_uom_id or default_uom,
        )
        if gross_weight and net_weight and gross_weight_uom != net_weight_uom:
            # Need a common UoM to show in the e-invoice:
            # use the smallest one
            # and convert the other weight
            if gross_weight_uom.factor > net_weight_uom.factor:
                common_uom = gross_weight_uom
                net_weight = net_weight_uom._compute_quantity(net_weight, common_uom)
            else:
                common_uom = net_weight_uom
                gross_weight = gross_weight_uom._compute_quantity(
                    gross_weight, common_uom
                )
        else:
            common_uom = gross_weight_uom if gross_weight else net_weight_uom

        return {
            "accompanying_common_uom": common_uom,
            "accompanying_gross_weight": gross_weight,
            "accompanying_net_weight": net_weight,
        }

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values=pdf_values)
        res["accompanying_carrier_info"] = (
            self.delivery_carrier_id._l10n_it_edi_get_values()
        )
        if weights_vals := self._l10n_it_edi_accompanying_get_weights():
            res.update(weights_vals)
        return res
