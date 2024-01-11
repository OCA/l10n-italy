from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    note_ids = env["stock.delivery.note"].search(
        [("carrier_id", "!=", False), ("delivery_method_id", "!=", False)]
    )

    for note_id in note_ids:
        note_id.delivery_method_id.write({"partner_id": note_id.carrier_id.id})
