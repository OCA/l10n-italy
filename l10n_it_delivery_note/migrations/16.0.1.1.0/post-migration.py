from openupgradelib import openupgrade  # pylint: disable=W7936


@openupgrade.migrate()
def migrate(env, version):
    carriers = env["stock.delivery.note"].search([]).mapped("carrier_id")
    if carriers:
        carriers.write({"is_carrier": True})
