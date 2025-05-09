# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


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


def set_exclude_from_vat_settlements(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_tax SET exclude_from_vat_settlement = True
        WHERE vat_statement_account_id IS NULL;
        """,
    )
