#  Copyright 2026 Sergio Corato <https://github.com/sergiocorato>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.l10n_it_account.migration_tools import EXISTING_TAX_MAX_ID_PARAM
from odoo.addons.l10n_it_account_vat_period_end_settlement import hooks


@tagged("post_install", "-at_install")
class TestMigrationHook(TransactionCase):
    """Test ``post_absorb_old_module``, shared by the hook and the migration."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        # Legacy column of the module up to 16.0, dropped in 18.0.
        if not openupgrade.column_exists(
            cls.env.cr, "account_tax", "vat_statement_account_id"
        ):
            cls.env.cr.execute(
                "ALTER TABLE account_tax ADD COLUMN vat_statement_account_id integer"
            )
        cls.param = cls.env["ir.config_parameter"].sudo()
        cls.tax_old = cls.env["account.tax"].create(
            {
                "name": "Migration hook old tax",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "company_id": cls.env.company.id,
            }
        )
        cls.tax_new = cls.env["account.tax"].create(
            {
                "name": "Migration hook new tax",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "company_id": cls.env.company.id,
            }
        )

    def setUp(self):
        super().setUp()
        self.env["account.tax"].search([]).write(
            {"exclude_from_vat_settlements": False}
        )
        self.param.search([("key", "=", EXISTING_TAX_MAX_ID_PARAM)]).unlink()

    def test_marker_restricts_exclusion(self):
        """Only the taxes existing before the 18.0 chart load are excluded."""
        self.param.set_param(EXISTING_TAX_MAX_ID_PARAM, str(self.tax_old.id))
        hooks.post_absorb_old_module(self.env)
        self.assertTrue(self.tax_old.exclude_from_vat_settlements)
        self.assertFalse(self.tax_new.exclude_from_vat_settlements)
        self.assertFalse(self.param.get_param(EXISTING_TAX_MAX_ID_PARAM))

    def test_no_marker_excludes_all(self):
        """Without the marker the 16.0 behaviour is kept (exclude all)."""
        hooks.post_absorb_old_module(self.env)
        self.assertTrue(self.tax_old.exclude_from_vat_settlements)
        self.assertTrue(self.tax_new.exclude_from_vat_settlements)
