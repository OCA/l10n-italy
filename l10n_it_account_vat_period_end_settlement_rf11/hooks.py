# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

OLD_MODULE = "account_vat_period_end_statement_rf11"
NEW_MODULE = "l10n_it_account_vat_period_end_settlement_rf11"


def pre_absorb_old_module(env):
    """Absorb the Odoo 16 module ``account_vat_period_end_statement_rf11``.

    On a v16->v18 upgrade the customer DB still carries the old module and its
    data. Every 74-ter field kept by this module lives on core/OCA models under
    an identical column name in both versions:

        account.tax                    : is_tax_74ter, tax_74ter_amount,
                                         tax_74_ter_income_account_id
        account.vat.period.end.statement:
                                         tax_74_ter_move_id, net_tax_74_ter,
                                         tax_74_ter_amount,
                                         tax_74_ter_amount_previous,
                                         tax_74_ter_amount_total

    so renaming the module (rather than letting the orphaned v16 module be
    uninstalled/purged, which would DROP those columns) preserves every value
    untouched and merely re-parents the old ``ir_model_data`` to us.

    Runs as ``pre_init_hook`` so it fires on the fresh-install path while the
    old module is still present. The base module
    ``l10n_it_account_vat_period_end_settlement`` (our dependency) absorbs the
    Odoo 16 ``account_vat_period_end_statement`` the same way and, being a
    dependency, is loaded before us -- so the base rename happens first.
    """
    if openupgrade.is_module_installed(env.cr, OLD_MODULE):
        openupgrade.update_module_names(
            env.cr,
            [(OLD_MODULE, NEW_MODULE)],
            merge_modules=True,
        )
