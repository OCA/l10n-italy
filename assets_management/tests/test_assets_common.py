# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import new_test_user
from odoo.tests.common import Form, SavepointCase


class TestAssets(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Companies
        cls.company_1 = cls.env.ref("base.main_company")
        cls.company_2 = cls.env["res.company"].create(
            {
                "name": "company 2",
            }
        )
        # User
        cls.user = new_test_user(
            cls.env,
            "user",
            groups="base.group_multi_company,account.group_account_manager",
            company_id=cls.company_1.id,
            company_ids=[(6, 0, [cls.company_1.id, cls.company_2.id])],
        )
        # Asset depreciation types
        cls.ad_type_civ_company_1 = cls.env.ref("assets_management.ad_type_civilistico")
        cls.ad_type_fis_company_1 = cls.env.ref("assets_management.ad_type_fiscale")
        cls.ad_type_civ_company_2 = cls.ad_type_civ_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        cls.ad_type_fis_company_2 = cls.ad_type_fis_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        # Asset depreciation modes
        cls.ad_mode_mat_company_1 = cls.env.ref("assets_management.ad_mode_materiale")
        cls.ad_mode_mat_company_2 = cls.ad_mode_mat_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        # Account types (non companies related)
        cls.data_account_type_current_assets = cls.env.ref(
            "account.data_account_type_current_assets"
        )
        cls.data_account_type_current_liabilities = cls.env.ref(
            "account.data_account_type_current_liabilities"
        )
        # Accounts
        cls.asset_account_company_1 = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_fixed_assets").id,
                ),
                ("company_id", "=", cls.company_1.id),
            ],
            limit=1,
        )
        cls.asset_account_company_2 = cls.asset_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )

        cls.depreciation_account_company_1 = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_expenses").id,
                ),
                ("company_id", "=", cls.company_1.id),
            ],
            limit=1,
        )
        cls.depreciation_account_company_2 = cls.depreciation_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )

        cls.fund_account_company_1 = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_non_current_assets").id,
                ),
                ("company_id", "=", cls.company_1.id),
            ],
            limit=1,
        )
        cls.fund_account_company_2 = cls.fund_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )

        cls.gain_account_company_1 = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                ),
                ("company_id", "=", cls.company_1.id),
            ],
            limit=1,
        )
        cls.gain_account_company_2 = cls.gain_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )

        cls.loss_account_company_1 = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_expenses").id,
                ),
                ("company_id", "=", cls.company_1.id),
            ],
            limit=1,
        )
        cls.loss_account_company_2 = cls.loss_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        cls.bank_account = cls.env["account.account"].create(
            {
                "code": "TBA",
                "name": "Test Bank Account",
                "user_type_id": cls.env.ref("account.data_account_type_liquidity").id,
            }
        )
        # Journals
        cls.journal_company_1 = cls.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", cls.company_1.id)],
            limit=1,
        )
        cls.journal_company_2 = cls.journal_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        # Asset categories
        cls.asset_category_1_company_1 = cls.env["asset.category"].create(
            {
                "name": "Asset category 1 Company 1",
                "company_id": cls.company_1.id,
                "asset_account_id": cls.asset_account_company_1.id,
                "depreciation_account_id": cls.depreciation_account_company_1.id,
                "fund_account_id": cls.fund_account_company_1.id,
                "gain_account_id": cls.gain_account_company_1.id,
                "journal_id": cls.journal_company_1.id,
                "loss_account_id": cls.loss_account_company_1.id,
                "type_ids": [
                    (
                        0,
                        0,
                        {
                            "depreciation_type_id": cls.ad_type_civ_company_1.id,
                            "mode_id": cls.ad_mode_mat_company_1.id,
                            "company_id": cls.company_1.id,
                        },
                    )
                ],
            }
        )

        cls.asset_category_1_company_2 = cls.env["asset.category"].create(
            {
                "name": "Asset category 1 Company 2",
                "company_id": cls.company_2.id,
                "asset_account_id": cls.asset_account_company_2.id,
                "depreciation_account_id": cls.depreciation_account_company_2.id,
                "fund_account_id": cls.fund_account_company_2.id,
                "gain_account_id": cls.gain_account_company_2.id,
                "journal_id": cls.journal_company_2.id,
                "loss_account_id": cls.loss_account_company_2.id,
                "type_ids": [
                    (
                        0,
                        0,
                        {
                            "depreciation_type_id": cls.ad_type_civ_company_2.id,
                            "mode_id": cls.ad_mode_mat_company_2.id,
                            "company_id": cls.company_2.id,
                        },
                    )
                ],
            }
        )
        # Tax accounts
        cls.tax_account_company_1 = cls.env["account.account"].create(
            {
                "name": "Deductable tax",
                "code": "DEDTAX",
                "user_type_id": cls.data_account_type_current_assets.id,
                "company_id": cls.company_1.id,
            }
        )
        cls.tax_account_company_2 = cls.tax_account_company_1.copy(
            {"company_id": cls.company_2.id}
        )
        # Taxes
        cls.tax_22_partial_60 = cls.env["account.tax"].create(
            {
                "name": "22% deductable partial 60%",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 22,
                "invoice_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 60,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account_company_1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 40,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 60,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account_company_1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 40,
                            "repartition_type": "tax",
                        },
                    ),
                ],
            }
        )

    def _create_asset(self, asset_date=None):
        asset = self.env["asset.asset"].create(
            {
                "name": "Test asset",
                "category_id": self.asset_category_1_company_1.id,
                "company_id": self.env.ref("base.main_company").id,
                "currency_id": self.env.ref("base.main_company").currency_id.id,
                "purchase_amount": 1000.0,
                "purchase_date": asset_date,
            }
        )
        return asset

    def _depreciate_asset(self, asset, date_dep):
        wiz_vals = asset.with_context(
            {"allow_reload_window": True}
        ).launch_wizard_generate_depreciations()
        wiz = (
            self.env["wizard.asset.generate.depreciation"]
            .with_context(wiz_vals["context"])
            .create({"date_dep": date_dep})
        )
        wiz.do_generate()

    def _create_purchase_invoice(self, invoice_date, tax_ids=False, amount=7000):
        invoice_line_vals = {
            "account_id": self.asset_category_1_company_1.asset_account_id.id,
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
                "journal_id": self.env["account.journal"]
                .search(
                    [
                        ("type", "=", "purchase"),
                    ],
                    limit=1,
                )
                .id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        invoice_line_vals,
                    )
                ],
            }
        )
        purchase_invoice.action_post()
        self.assertEqual(purchase_invoice.state, "posted")
        return purchase_invoice

    def _create_entry(self, account, amount, post=True):
        """Create an entry that adds `amount` to `account`."""
        entry_form = Form(self.env["account.move"])
        with entry_form.line_ids.new() as asset_line:
            asset_line.account_id = account
            asset_line.debit = amount
        with entry_form.line_ids.new() as bank_line:
            bank_line.account_id = self.bank_account
        entry = entry_form.save()

        if post:
            entry.action_post()

        self.assertEqual(entry.move_type, "entry")
        return entry

    def _update_asset(self, entry, asset):
        """Execute the wizard on `entry` to update `asset`."""
        wizard_action = entry.open_wizard_manage_asset()
        wizard_model = self.env[wizard_action["res_model"]]
        wizard_context = wizard_action["context"]

        wizard_form = Form(wizard_model.with_context(**wizard_context))
        wizard_form.management_type = "update"
        wizard_form.asset_id = asset
        wizard = wizard_form.save()

        return wizard.link_asset()
