from odoo import api, fields, models


class AccountTaxKind(models.Model):
    _name = "account.tax.kind"
    _description = "Tax exemption kind"
    _rec_names_search = ["code", "name"]

    code = fields.Char(size=4, required=True)
    name = fields.Char(required=True)

    @api.depends("code", "name")
    def _compute_display_name(self):
        for tax_kind in self:
            tax_kind.display_name = f"[{tax_kind.code}] {tax_kind.name}"
