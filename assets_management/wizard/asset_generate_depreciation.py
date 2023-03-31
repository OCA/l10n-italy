# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _name = "wizard.asset.generate.depreciation"
    _description = "Generate Asset Depreciations"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_date_dep(self):
        fiscal_year = self.env["account.fiscal.year"].get_fiscal_year_by_date(
            fields.Date.today(), company=self.env.user.company_id, miss_raise=False
        )
        if fiscal_year:
            return fiscal_year.date_to
        return fields.Date.today()

    @api.model
    def get_default_type_ids(self):
        return [(6, 0, self.env["asset.depreciation.type"].search([]).ids)]

    asset_ids = fields.Many2many(
        "asset.asset",
        string="Assets",
    )

    category_ids = fields.Many2many(
        "asset.category",
        string="Categories",
    )

    company_id = fields.Many2one(
        "res.company",
        default=get_default_company_id,
        string="Company",
    )

    date_dep = fields.Date(
        default=get_default_date_dep,
        required=True,
        string="Depreciation Date",
    )

    type_ids = fields.Many2many(
        "asset.depreciation.type",
        default=get_default_type_ids,
        required=True,
        string="Depreciation Types",
    )

    def do_generate(self):
        """
        Launches the generation of new depreciation lines for the retrieved
        assets.
        Reloads the current window if necessary.
        """
        self.ensure_one()
        # Add depreciation date in context just in case
        deps = self.get_depreciations().with_context(dep_date=self.date_dep)
        dep_lines = deps.generate_depreciation_lines(self.date_dep)
        deps.post_generate_depreciation_lines(dep_lines)
        if self._context.get("reload_window"):
            return {"type": "ir.actions.client", "tag": "reload"}

    def get_depreciations(self):
        self.ensure_one()
        domain = self.get_depreciations_domain()
        return self.env["asset.depreciation"].search(domain)

    def get_depreciations_domain(self):
        domain = [
            ("amount_residual", ">", 0),
            ("date_start", "!=", False),
            ("date_start", "<", self.date_dep),
            ("type_id", "in", self.type_ids.ids),
        ]
        if self.asset_ids:
            domain += [("asset_id", "in", self.asset_ids.ids)]
        if self.category_ids:
            domain += [("asset_id.category_id", "in", self.category_ids.ids)]
        if self.company_id:
            domain += [("company_id", "=", self.company_id.id)]
        return domain
