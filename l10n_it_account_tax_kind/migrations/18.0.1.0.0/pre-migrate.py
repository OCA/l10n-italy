# Dinamiche Aziendali srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import SUPERUSER_ID, api

MODEL = "account.tax"
OLD_MODEL = "account.tax.kind"
RENAMED_FIELDS = [
    (
        "law_reference",
        "l10n_it_law_reference",
    ),
]


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    openupgrade.logged_query(
        env.cr,
        sql.SQL(f"""
            UPDATE
                {MODEL.replace(".", "_")}
            SET
                l10n_it_exempt_reason = kind_id.code
            FROM
                {OLD_MODEL.replace(".", "_")} AS kind
            WHERE
                {MODEL.replace(".", "_")}.kind_id = kind.id
                AND {MODEL.replace(".", "_")}.kind_id IS NOT NULL
        """),
    )

    field_spec = []
    for renamed_field in RENAMED_FIELDS:
        old_field, new_field = renamed_field
        field_spec.append(
            (
                MODEL,
                MODEL.replace(".", "_"),
                old_field,
                new_field,
            )
        )
    openupgrade.rename_fields(
        env,
        field_spec,
    )

    module = env["ir.module.module"].search([("name", "=", "l10n_it_account_tax_kind")])
    module.button_immediate_uninstall()
