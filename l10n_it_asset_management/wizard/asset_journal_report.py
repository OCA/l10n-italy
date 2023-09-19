# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class WizardAssetJournalReport(models.TransientModel):
    _name = "wizard.asset.journal.report"
    _description = "Wizard Asset Journal Report"

    @api.model
    def get_asset_order_fname_selection(self):
        fnames = ["code", "name"]
        asset_fields = self.env["asset.asset"]._fields
        return [(fname, asset_fields[fname].string) for fname in fnames]

    @api.model
    def get_default_asset_order_fname(self):
        vals = self._fields["asset_order_fname"].get_values(self.env)
        if vals:
            return vals[0]
        return

    @api.model
    def get_default_category_ids(self):
        return self.env["asset.category"].search([("print_by_default", "=", True)])

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_date(self):
        return date(date.today().year - 1, 12, 31)

    @api.model
    def get_default_report_footer_year(self):
        return str(date.today().year)

    @api.model
    def get_default_type_ids(self):
        return self.env["asset.depreciation.type"].search(
            [("print_by_default", "=", True)]
        )

    asset_ids = fields.Many2many("asset.asset", string="Assets")

    asset_order_fname = fields.Selection(
        get_asset_order_fname_selection,
        default=get_default_asset_order_fname,
        required=True,
        string="Asset Print Order",
    )

    category_ids = fields.Many2many(
        "asset.category", default=get_default_category_ids, string="Categories"
    )

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, required=True, string="Company"
    )

    date = fields.Date(
        default=get_default_date,
        string="To Date",
    )

    show_totals = fields.Boolean(default=True)

    show_category_totals = fields.Boolean(default=True)
    show_sold_assets = fields.Boolean()
    report_footer_year = fields.Char(default=get_default_report_footer_year)

    type_ids = fields.Many2many(
        "asset.depreciation.type",
        default=get_default_type_ids,
        string="Depreciation Types",
    )

    @api.onchange("category_ids", "company_id", "date", "type_ids")
    def onchange_assets(self):
        self.asset_ids = self.filter_assets()
        return {"domain": {"asset_ids": self.get_asset_domain()}}

    def button_export_asset_journal_html(self):
        self.ensure_one()
        return self.export_asset_journal_report("qweb-html")

    def button_export_asset_journal_pdf(self):
        self.ensure_one()
        return self.export_asset_journal_report("qweb-pdf")

    def button_export_asset_journal_xlsx(self):
        self.ensure_one()
        return self.export_asset_journal_report("xlsx")

    def export_asset_journal_report(self, report_type=None):
        self.ensure_one()
        report_obj = self.env["report_asset_journal"]
        report_vals = self.prepare_report_vals()
        report = report_obj.create(report_vals)
        report.compute_data_for_report()
        return report.print_report(report_type)

    def filter_assets(self):
        assets = self.asset_ids
        if self.category_ids:
            assets = assets.filtered(
                lambda a: a.category_id.id in self.category_ids.ids
            )
        if self.company_id:
            assets = assets.filtered(
                lambda a: a.company_id.id in (False, self.company_id.id)
            )
        if self.date:
            assets = assets.filtered(lambda a: a.purchase_date <= self.date)
        if self.type_ids:
            assets = assets.filtered(
                lambda a: any(
                    [d.type_id.id in self.type_ids.ids for d in a.depreciation_ids]
                )
            )
        return assets

    def get_asset_domain(self):
        asset_domain = []
        if self.category_ids:
            asset_domain.append(("category_id", "in", self.category_ids.ids))
        if self.company_id:
            asset_domain.append(("company_id", "in", (False, self.company_id.id)))
        if self.date:
            asset_domain.append(("purchase_date", "<=", self.date))
        if self.type_ids:
            deps = self.env["asset.depreciation"].search(
                [("type_id", "in", self.type_ids.ids)]
            )
            asset_domain.append(("id", "in", deps.mapped("asset_id").ids))
        return asset_domain

    def prepare_report_vals(self):
        self.ensure_one()
        return {
            "asset_ids": [(6, 0, self.asset_ids.ids)],
            "asset_order_fname": self.asset_order_fname,
            "category_ids": [(6, 0, self.category_ids.ids)],
            "company_id": self.company_id.id,
            "date": self.date,
            "show_totals": self.show_totals,
            "show_category_totals": self.show_category_totals,
            "show_sold_assets": self.show_sold_assets,
            "report_footer_year": self.report_footer_year,
            "type_ids": [(6, 0, self.type_ids.ids)],
        }
