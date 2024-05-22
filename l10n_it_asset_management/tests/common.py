# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.fields import Command, first
from odoo.tests.common import TransactionCase


class Common(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data_account_type_current_assets = "asset_current"

        cls.asset_fixed_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "asset_fixed",
                )
            ],
            limit=1,
        )
        cls.expense_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "expense",
                )
            ],
            limit=1,
        )
        cls.asset_non_current_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "asset_non_current",
                )
            ],
            limit=1,
        )
        cls.income_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "income",
                )
            ],
            limit=1,
        )

        cls.general_journal = cls.env["account.journal"].search(
            [("type", "=", "general")], limit=1
        )
        cls.purchase_journal = cls.env["account.journal"].search(
            [
                ("type", "=", "purchase"),
            ],
            limit=1,
        )

        cls.civilistico_asset_dep_type = cls.env.ref(
            "l10n_it_asset_management.ad_type_civilistico"
        )

        cls.materiale_asset_dep_mode = cls.env.ref(
            "l10n_it_asset_management.ad_mode_materiale"
        )

        cls.asset_category_1 = cls.env["asset.category"].create(
            {
                "name": "Asset category 1",
                "asset_account_id": cls.asset_fixed_account.id,
                "depreciation_account_id": cls.expense_account.id,
                "fund_account_id": cls.asset_non_current_account.id,
                "gain_account_id": cls.income_account.id,
                "journal_id": cls.general_journal.id,
                "loss_account_id": cls.expense_account.id,
                "type_ids": [
                    Command.create(
                        {
                            "depreciation_type_id": cls.civilistico_asset_dep_type.id,
                            "mode_id": cls.materiale_asset_dep_mode.id,
                        },
                    )
                ],
            }
        )
        cls.tax_account = cls.env["account.account"].create(
            {
                "name": "Deductable tax",
                "code": "DEDTAX",
                "account_type": cls.data_account_type_current_assets,
            }
        )
        cls.tax_22_partial_60 = cls.env["account.tax"].create(
            {
                "name": "22% deductable partial 60%",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 22,
                "invoice_repartition_line_ids": [
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 60,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account.id,
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 40,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 60,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account.id,
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 40,
                            "repartition_type": "tax",
                        },
                    ),
                ],
            }
        )

    def _create_asset(self, asset_date):
        asset = self.env["asset.asset"].create(
            {
                "name": "Test asset",
                "category_id": self.asset_category_1.id,
                "company_id": self.env.ref("base.main_company").id,
                "currency_id": self.env.ref("base.main_company").currency_id.id,
                "purchase_amount": 1000.0,
                "purchase_date": asset_date,
            }
        )
        return asset

    def _depreciate_asset(self, asset, date_dep):
        wiz_vals = asset.with_context(
            **{"allow_reload_window": True}
        ).launch_wizard_generate_depreciations()
        wiz = (
            self.env["wizard.asset.generate.depreciation"]
            .with_context(**wiz_vals["context"])
            .create({"date_dep": date_dep})
        )
        wiz.do_generate()

    def _create_purchase_invoice(self, invoice_date, tax_ids=False, amount=7000):
        invoice_line_vals = {
            "account_id": self.asset_category_1.asset_account_id.id,
            "quantity": 1,
            "price_unit": amount,
        }
        if tax_ids:
            invoice_line_vals.update({"tax_ids": tax_ids})
        purchase_invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "invoice_date": invoice_date,
                "partner_id": self.env.ref("base.partner_demo").id,
                "journal_id": self.purchase_journal.id,
                "invoice_line_ids": [
                    Command.create(
                        invoice_line_vals,
                    )
                ],
            }
        )
        purchase_invoice.action_post()
        self.assertEqual(purchase_invoice.state, "posted")
        return purchase_invoice

    def _civil_depreciate_asset(self, asset):
        # Keep only one civil depreciation
        civil_depreciation = first(
            asset.depreciation_ids.filtered(
                lambda d: d.type_id == self.civilistico_asset_dep_type
            )
        )
        (asset.depreciation_ids - civil_depreciation).unlink()

        civil_depreciation.line_ids = [
            Command.clear(),
            Command.create(
                {
                    "name": "2019",
                    "date": date(2019, 12, 31),
                    "move_type": "depreciated",
                    "amount": 500,
                },
            ),
            Command.create(
                {
                    "name": "2020",
                    "date": date(2020, 12, 31),
                    "move_type": "depreciated",
                    "amount": 500,
                },
            ),
        ]
        return True

    def _generate_fiscal_years(self, start_date, end_date):
        fiscal_years = range(
            start_date.year,
            end_date.year,
        )
        fiscal_years_values = list()
        for fiscal_year in fiscal_years:
            fiscal_year_values = {
                "name": "Fiscal Year %d" % fiscal_year,
                "date_from": date(fiscal_year, 1, 1),
                "date_to": date(fiscal_year, 12, 31),
            }
            fiscal_years_values.append(fiscal_year_values)
        return self.env["account.fiscal.year"].create(fiscal_years_values)

    def _get_report_values(self, report_type):
        if report_type == "previsional":
            wizard_model = "wizard.asset.previsional.report"
            report_model = "report_asset_previsional"
            export_method = "export_asset_previsional_report"
        elif report_type == "journal":
            wizard_model = "wizard.asset.journal.report"
            report_model = "report_asset_journal"
            export_method = "export_asset_journal_report"
        else:
            raise Exception("Report can only be 'journal' or 'previsional'")
        return export_method, report_model, wizard_model

    def _get_report(self, report_date, report_type):
        export_method, report_model, wizard_model = self._get_report_values(report_type)

        wiz = self.env[wizard_model].create(
            {
                "date": report_date,
            }
        )
        report_result = getattr(wiz, export_method)()
        report_ids = report_result["context"]["report_action"]["context"]["active_ids"]
        report = self.env[report_model].browse(report_ids)
        return report
