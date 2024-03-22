#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

MODEL_TO_RENAMED_FIELDS = {
    "asset.depreciation.mode.line": [
        ("from_nr", "from_year_nr"),
        ("to_nr", "to_year_nr"),
    ]
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
