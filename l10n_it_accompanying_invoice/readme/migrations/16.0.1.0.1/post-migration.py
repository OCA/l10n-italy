#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from .hooks import RENAMED_FIELDS


def _get_set_clause(fields_list):
    set_fields_list = [f"{field[1]} = ai.{field[0]}" for field in fields_list]
    set_fields_clause = ", ".join(set_fields_list)
    return set_fields_clause


def migrate(cr, installed_version):
    fields_list = [(field[0][1], field[1][1]) for field in RENAMED_FIELDS]
    set_fields_clause = _get_set_clause(fields_list)
    query = f"""
UPDATE account_move am
SET {set_fields_clause}
FROM account_invoice ai
WHERE am.old_invoice_id = ai.id
    """
    openupgrade.logged_query(cr, query)
