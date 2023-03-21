# Copyright 2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def create_withholding_data_lines(env):
    # create ftpa_withholding_ids from ftpa_withholding_type and ftpa_withholding_amount
    openupgrade.logged_query(
        env.cr, """
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
                ai.ftpa_withholding_type,
                ai.ftpa_withholding_amount,
                ai.id,
                ai.create_uid,
                ai.create_date,
                ai.write_date,
                ai.write_uid
            FROM account_invoice ai
            WHERE ai.ftpa_withholding_type IS NOT NULL;
            """
    )


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    create_withholding_data_lines(env)
