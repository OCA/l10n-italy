# Copyright 2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2 import sql


def create_withholding_data_lines(env):
    # create ftpa_withholding_ids from ftpa_withholding_type and ftpa_withholding_amount
    column_name = openupgrade.get_legacy_name('ftpa_withholding_amount')
    if openupgrade.column_exists(env.cr, 'account_invoice', column_name):
        openupgrade.logged_query(
            env.cr, sql.SQL(
                """
                INSERT INTO withholding_data_line
                (
                    name,
                    amount,
                    invoice_id,
                    create_uid,
                    create_date,
                    write_date,
                    write_uid
                )
                SELECT
                    ai.{ftpa_withholding_type},
                    ai.{ftpa_withholding_amount},
                    ai.id,
                    ai.create_uid,
                    ai.create_date,
                    ai.write_date,
                    ai.write_uid
                FROM account_invoice ai
                WHERE ai.{ftpa_withholding_type} IS NOT NULL;
                """
                ).format(
                    ftpa_withholding_type=sql.Identifier(
                        openupgrade.get_legacy_name(
                            'ftpa_withholding_type')
                    ),
                    ftpa_withholding_amount=sql.Identifier(
                        openupgrade.get_legacy_name(
                            'ftpa_withholding_amount')
                    ),
                )
            )
    else:
        openupgrade.logged_query(
            env.cr, sql.SQL(
                """
                INSERT INTO withholding_data_line
                (
                    name,
                    invoice_id,
                    create_uid,
                    create_date,
                    write_date,
                    write_uid
                )
                SELECT
                    ai.{ftpa_withholding_type},
                    ai.id,
                    ai.create_uid,
                    ai.create_date,
                    ai.write_date,
                    ai.write_uid
                FROM account_invoice ai
                WHERE ai.{ftpa_withholding_type} IS NOT NULL;
                """
            ).format(
                ftpa_withholding_type=sql.Identifier(
                    openupgrade.get_legacy_name(
                        'ftpa_withholding_type')
                ),
            )
        )


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    create_withholding_data_lines(env)
