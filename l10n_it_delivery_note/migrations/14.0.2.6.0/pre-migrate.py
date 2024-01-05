from collections import defaultdict

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Get every carrier that was a 'res.partner' and create a 'delivery.carrier'
    env.cr.execute(
        """SELECT id, carrier_id
        FROM stock_delivery_note
        WHERE carrier_id IS NOT NULL"""
    )
    res = env.cr.dictfetchall()

    # Group by carrier_id to not create duplicates
    new_res = defaultdict(list)
    for i in res:
        new_res[i.get("carrier_id")].append(i.get("id"))

    for (carrier_id, delivery_note_ids) in new_res.items():
        partner_carrier_id = env["res.partner"].browse(carrier_id)

        carrier_product = env["product.product"].create(
            {
                "name": partner_carrier_id.name,
                "type": "service",
                "sale_ok": False,
                "purchase_ok": False,
                "list_price": 0.0,
                "invoice_policy": "order",
            }
        )

        delivery_carrier_id = env["delivery.carrier"].create(
            {
                "name": partner_carrier_id.name,
                "company_id": partner_carrier_id.company_id.id,
                "country_ids": [(4, partner_carrier_id.country_id.id)]
                if partner_carrier_id.country_id
                else [],
                "state_ids": [(4, partner_carrier_id.state_id.id)]
                if partner_carrier_id.state_id
                else [],
                "zip_from": partner_carrier_id.zip,
                "zip_to": partner_carrier_id.zip,
                "product_id": carrier_product.id,
            }
        )

        # If it's only one add a duplicate to
        # delivery note ids otherwise it would
        # be casted to tuple as '(id,)' and that will raise an error
        if len(delivery_note_ids) == 1:
            delivery_note_ids.append(delivery_note_ids[0])

        # Update carrier in 'stock.picking'
        openupgrade.logged_query(
            env.cr,
            """UPDATE stock_picking
             SET carrier_id={}
             WHERE delivery_note_id IN {}""".format(
                delivery_carrier_id.id, tuple(delivery_note_ids)
            ),
        )

        # Remove carrier from delivery notes
        openupgrade.logged_query(
            env.cr,
            """UPDATE stock_delivery_note
             SET carrier_id=NULL
             WHERE id IN {}""".format(
                tuple(delivery_note_ids)
            ),
        )
