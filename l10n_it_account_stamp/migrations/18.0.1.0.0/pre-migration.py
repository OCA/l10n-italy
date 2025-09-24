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
                "tax_stamp",
                "l10n_it_account_stamp_is_stamp_duty_applied",
            ),
            (
                "account.move",
                "account_move",
                "tax_stamp_line_present",
                "l10n_it_account_stamp_is_stamp_duty_present",
            ),
            (
                "account.move",
                "account_move",
                "auto_compute_stamp",
                "l10n_it_account_stamp_auto_compute_stamp_duty",
            ),
            (
                "account.move",
                "account_move",
                "manually_apply_tax_stamp",
                "l10n_it_account_stamp_manually_apply_stamp_duty",
            ),
            (
                "res.company",
                "res_company",
                "tax_stamp_product_id",
                "l10n_it_account_stamp_stamp_duty_product_id",
            ),
            (
                "res.config.settings",
                "res_config_settings",
                "tax_stamp_product_id",
                "l10n_it_account_stamp_stamp_duty_product_id",
            ),
            (
                "product.template",
                "product_template",
                "stamp_apply_tax_ids",
                "l10n_it_account_stamp_stamp_duty_apply_tax_ids",
            ),
            (
                "product.template",
                "product_template",
                "stamp_apply_min_total_base",
                "l10n_it_account_stamp_tax_apply_min_total_base",
            ),
            (
                "product.template",
                "product_template",
                "is_stamp",
                "l10n_it_account_stamp_is_stamp",
            ),
            (
                "product.template",
                "product_template",
                "auto_compute",
                "l10n_it_account_stamp_auto_compute",
            ),
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    _rename_fields(env)
