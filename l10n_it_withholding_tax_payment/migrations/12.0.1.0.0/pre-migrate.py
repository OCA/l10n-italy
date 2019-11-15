# Copyright 2019 Matteo Bilotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from datetime import datetime
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


def _fix_date_field(cr):
    cr.execute("SELECT id, date FROM withholding_tax_move_payment"
               " WHERE date IS NOT NULL;")

    records = cr.fetchall()
    for record in records:
        record_id = record[0]
        record_value = record[1]

        try:
            datetime.strptime(record_value, DEFAULT_SERVER_DATE_FORMAT)

        except (TypeError, ValueError):
            _logger.error("The row in table 'withholding_tax_move_payment'"
                          " with ID #{} and 'date' field valued"
                          " as '{}' will be set as NULL..."
                          .format(record_id, record_value))

            cr.execute("UPDATE withholding_tax_move_payment"
                       " SET date = NULL WHERE id = %s;", (record_id, ))

    cr.execute("ALTER TABLE withholding_tax_move_payment"
               " ALTER COLUMN date TYPE DATE USING date::DATE;")


def migrate(cr, version):
    if not version:
        _logger.warning("Does not exist any previous version for this module. "
                        "Skipping the migration...")

        return

    _fix_date_field(cr)

    _logger.info("Migration executed successfully. Exiting...")
