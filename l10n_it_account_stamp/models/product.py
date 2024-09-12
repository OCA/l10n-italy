# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, exceptions, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.constrains(
        "l10n_it_account_stamp_tax_stamp_apply_tax_ids",
        "l10n_it_account_stamp_is_stamp",
    )
    def _check_stamp_apply_tax(self):
        for template in self:
            if (
                template.l10n_it_account_stamp_tax_stamp_apply_tax_ids
                and not template.l10n_it_account_stamp_is_stamp
            ):
                raise exceptions.ValidationError(
                    _("The product %s must be a stamp to apply set taxes!")
                    % template.name
                )

    l10n_it_account_stamp_tax_stamp_apply_tax_ids = fields.Many2many(
        comodel_name="account.tax",
        relation="l10n_it_account_stamp_product_tax_account_tax_rel",
        column1="product_id",
        column2="tax_id",
        string="Stamp taxes",
    )
    l10n_it_account_stamp_tax_apply_min_total_base = fields.Float(
        string="Stamp applicability min total base",
        digits="Account",
    )
    l10n_it_account_stamp_is_stamp = fields.Boolean(
        string="Is a stamp",
    )
    l10n_it_account_stamp_auto_compute = fields.Boolean(
        string="Auto-compute",
    )
