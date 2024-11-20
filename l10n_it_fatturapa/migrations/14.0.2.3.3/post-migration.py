from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    attachments = env["fatturapa.attachments"].search(
        [
            ("res_model", "=", False),
            ("res_id", "=", False),
        ]
    )
    for att in attachments:
        att.write({"res_model": "fatturapa.attachments", "res_id": att.id})
