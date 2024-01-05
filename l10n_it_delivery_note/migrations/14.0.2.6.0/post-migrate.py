from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Sync every picking's carrier to their delivery_note
    picking_ids = env["stock.picking"].search(
        [("delivery_note_id", "!=", False), ("carrier_id", "!=", False)]
    )
    for picking in picking_ids:
        picking.delivery_note_id.carrier_id = picking.carrier_id
