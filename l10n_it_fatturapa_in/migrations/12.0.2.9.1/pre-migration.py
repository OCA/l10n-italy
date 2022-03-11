from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(
        env.cr, 'fatturapa_attachment_in', "is_self_invoice"
    ):
        openupgrade.add_fields(
            env,
            [(
                "is_self_invoice",
                "fatturapa.attachment.in",
                "fatturapa_attachment_in",
                "boolean",
                False,
                "l10n_it_fatturapa_in",
            )],
        )
