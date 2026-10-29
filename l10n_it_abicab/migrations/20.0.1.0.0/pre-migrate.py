# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Migrate ABI/CAB data from res.bank to res.partner.bank.

    In Odoo 20, res.bank has been removed and its fields merged into
    res.partner.bank.  In 19.0 the module stored ABI/CAB as:
      - res.bank:          abi, cab          (source fields)
      - res.partner.bank:  bank_abi, bank_cab (stored related via bank_id)

    The stored related columns may be stale if the bank was edited after
    the partner-bank record was created, so we refresh them from res_bank
    before the table disappears.
    """
    if not version:
        return

    cr.execute(
        """
        SELECT column_name
          FROM information_schema.columns
         WHERE (table_name = 'res_bank' AND column_name IN ('abi', 'cab'))
            OR (table_name = 'res_partner_bank' AND column_name = 'bank_id')
        """
    )
    existing = {row[0] for row in cr.fetchall()}
    if not ({"abi", "cab", "bank_id"} <= existing):
        _logger.info(
            "res_bank.abi/cab or res_partner_bank.bank_id missing — "
            "nothing to migrate (columns found: %s)",
            existing,
        )
        return

    # Ensure target columns exist (they should from the stored related,
    # but be defensive for fresh installs that jump straight to 20.0).
    for col in ("bank_abi", "bank_cab"):
        cr.execute(
            """
            SELECT 1
              FROM information_schema.columns
             WHERE table_name = 'res_partner_bank'
               AND column_name = %s
            """,
            (col,),
        )
        if not cr.fetchone():
            cr.execute(
                f"ALTER TABLE res_partner_bank ADD COLUMN {col} varchar"
            )

    cr.execute(
        """
        UPDATE res_partner_bank pb
           SET bank_abi = rb.abi,
               bank_cab = rb.cab
          FROM res_bank rb
         WHERE pb.bank_id = rb.id
           AND (rb.abi IS NOT NULL OR rb.cab IS NOT NULL)
        """
    )
    _logger.info(
        "Migrated ABI/CAB from res_bank to res_partner_bank (%d rows)",
        cr.rowcount,
    )
