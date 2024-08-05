import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "account_move_line", "old_delivery_note_id"):
        openupgrade.m2o_to_x2m(
            env.cr,
            model=env["account.move.line"],
            table="account_move_line",
            field="delivery_note_ids",
            source_field="old_delivery_note_id",
        )

    query = (
        "SELECT id "
        "FROM account_move_line "
        "WHERE display_type is null "
        "AND old_delivery_note_id is not null"
    )
    openupgrade.logged_query(env.cr, query)
    ml_ids = [x for (x,) in env.cr.fetchall()]
    # batch to avoid MemoryError with large datasets
    i = 0
    batch_size = 200
    while ml_id_batch := ml_ids[i : i + batch_size]:
        i += batch_size
        move_lines = env["account.move.line"].browse(ml_id_batch)
        for ml in move_lines:
            # Reasonable guess at linking delivery note lines based on faulty data
            # Get the Delivery notes that are linked
            # both to the invoice and to the move_line via sales order line
            # Also consider the old delivery_note_id
            relevant_dns = (
                ml.move_id.delivery_note_ids
                & ml.mapped("sale_line_ids.delivery_note_line_ids.delivery_note_id")
            ) | ml.delivery_note_id
            # Of all those delivery notes, get the lines with the same product
            relevant_dn_lines = relevant_dns.mapped("line_ids").filtered(
                lambda x, ml=ml: x.product_id == ml.product_id
            )
            try:
                ml.write(
                    {
                        "delivery_note_line_ids": [(6, 0, relevant_dn_lines.ids)],
                        "delivery_note_ids": False,
                    }
                )
            except Exception:
                _logger.error("Error while writing on " + str(ml), exc_info=True)
        env.cache.invalidate()
