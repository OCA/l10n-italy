#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, installed_version):
    phone_column = 'phone_electronic_invoice'
    old_phone_column = openupgrade.get_legacy_name(phone_column)
    openupgrade.move_field_m2o(
        env.cr,
        env,
        'res.company', old_phone_column, 'partner_id',
        'res.partner', phone_column,
    )
