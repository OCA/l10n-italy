# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def post_absorb_old_module(env):
    if openupgrade.column_exists(env.cr, "account_tax", "vat_statement_account_id"):
        query = """
            UPDATE account_tax SET exclude_from_vat_settlements = True
            WHERE vat_statement_account_id IS NULL;
        """
        openupgrade.logged_query(env.cr, query)


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "account_vat_period_end_statement"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "account_vat_period_end_statement",
                    "l10n_it_account_vat_period_end_settlement",
                ),
            ],
            merge_modules=True,
        )
