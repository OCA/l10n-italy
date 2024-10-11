#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def _rename_fields(env):
    openupgrade.rename_fields(
        env,
        [
            (
                "account.move",
                "account_move",
                "l10n_it_account_stamp_is_tax_stamp_applied",
                "l10n_it_account_stamp_is_stamp_duty_applied",
            ),
            (
                "account.move",
                "account_move",
                "l10n_it_account_stamp_is_tax_stamp_present",
                "l10n_it_account_stamp_is_stamp_duty_present",
            ),
            (
                "account.move",
                "account_move",
                "l10n_it_account_stamp_auto_compute_tax_stamp",
                "l10n_it_account_stamp_auto_compute_stamp_duty",
            ),
            (
                "account.move",
                "account_move",
                "l10n_it_account_stamp_manually_apply_tax_stamp",
                "l10n_it_account_stamp_manually_apply_stamp_duty",
            ),
            (
                "res.company",
                "res_company",
                "l10n_it_account_stamp_tax_stamp_product_id",
                "l10n_it_account_stamp_stamp_duty_product_id",
            ),
            (
                "res.config.settings",
                "res_config_settings",
                "l10n_it_account_stamp_tax_stamp_product_id",
                "l10n_it_account_stamp_stamp_duty_product_id",
            ),
            (
                "product.template",
                "product_template",
                "l10n_it_account_stamp_tax_stamp_apply_tax_ids",
                "l10n_it_account_stamp_stamp_duty_apply_tax_ids",
            ),
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    _rename_fields(env)
