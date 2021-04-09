# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, exceptions, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.constrains("stamp_apply_tax_ids", "is_stamp")
    def _check_stamp_apply_tax(self):
        for template in self:
            if template.stamp_apply_tax_ids and not template.is_stamp:
                raise exceptions.ValidationError(
                    _("The product %s must be a stamp to apply set taxes!")
                    % template.name
                )

    stamp_apply_tax_ids = fields.Many2many(
        "account.tax",
        "product_tax_account_tax__rel",
        "product_id",
        "tax_id",
        string="Stamp taxes",
    )
    stamp_apply_min_total_base = fields.Float(
        "Stamp applicability min total base", digits="Account"
    )
    is_stamp = fields.Boolean("Is a stamp")
    auto_compute = fields.Boolean("Auto-compute")
