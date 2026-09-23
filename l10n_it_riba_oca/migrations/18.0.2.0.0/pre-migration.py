#  Copyright 2026 Lorenzo Battistini
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Slip lines are not paid one by one any more.

    The collection is tracked on the whole slip, through the reconciliation
    of the credit towards the bank, so the lines go back to the state they
    had before the settlement entries that this version does not create.
    The slips keep their state: the ones whose collection has actually been
    reconciled stay paid, the other ones are shown as still to be collected.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE riba_slip_line line
        SET state = CASE
            WHEN config.type = 'sbf' THEN 'credited'
            ELSE 'confirmed'
        END
        FROM riba_slip slip
        LEFT JOIN riba_configuration config ON config.id = slip.config_id
        WHERE line.slip_id = slip.id
          AND line.state = 'paid'
        """,
    )
