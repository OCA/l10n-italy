# Copyright Lorenzo Carta - Innovyou
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

MODEL_TO_RENAMED_FIELDS = {
    "account.move": [
        ("asset_ids", "l10n_it_asset_ids"),
    ],
    "account.move.line": [
        ("asset_ids", "l10n_it_asset_ids"),
    ],
    "asset.accounting.info": [
        ("asset_id", "l10n_it_asset_id"),
    ],
    "asset.depreciation": [
        ("asset_id", "l10n_it_asset_id"),
    ],
    "asset.depreciation.line": [
        ("asset_id", "l10n_it_asset_id"),
    ],
}


def _rename_fields(env):
    openupgrade.rename_fields(
        env,
        [
            (
                model_name,
                model_name.replace(".", "_"),
                field_spec[0],
                field_spec[1],
            )
            for model_name, field_specs in MODEL_TO_RENAMED_FIELDS.items()
            for field_spec in field_specs
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    _rename_fields(env)
