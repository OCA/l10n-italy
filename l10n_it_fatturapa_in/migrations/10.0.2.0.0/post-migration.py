# Copyright 2020 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2020 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2 import sql


def create_withholding_data_lines(env):
    """
    Create ftpa_withholding_ids from ftpa_withholding_type
    and ftpa_withholding_amount
    """
    column_wht_amount = openupgrade.get_legacy_name('ftpa_withholding_amount')
    column_wht_type = openupgrade.get_legacy_name('ftpa_withholding_type')
    exists = openupgrade.column_exists(env.cr, 'account_invoice', column_wht_amount)
    mapping = {
        'name': 'ai.{ftpa_withholding_type}'.format(
            ftpa_withholding_type=column_wht_type),
        'invoice_id': 'ai.id',
        'create_uid': 'ai.create_uid',
        'create_date': 'ai.create_date',
        'write_date': 'ai.write_date',
        'write_uid': 'ai.write_uid',
    }
    if exists:
        mapping.update(
            {'amount': 'ai.{ftpa_withholding_amount}'.format(
                ftpa_withholding_amount=column_wht_amount)})
    query = """
        INSERT INTO withholding_data_line
        ({columns})
        SELECT {values}
        FROM account_invoice AS ai
        WHERE ai.{ftpa_withholding_type} IS NOT NULL;""".format(
            columns=','.join(mapping.keys()),
            values=','.join(mapping.values()),
            ftpa_withholding_type=column_wht_type)
    openupgrade.logged_query(env.cr, sql.SQL(query))


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    create_withholding_data_lines(env)
