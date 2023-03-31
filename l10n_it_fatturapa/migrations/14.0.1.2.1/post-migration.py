from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return

    query = """
            UPDATE res_company
            SET fatturapa_preview_style = %s
            WHERE fatturapa_preview_style = %s;
        """

    env.cr.execute(
        query,
        (
            "Foglio_di_stile_fatturaordinaria_v1.2.2.xsl",
            "fatturaordinaria_v1.2.1.xsl",
        ),
    )

    env.cr.execute(
        query,
        (
            "FoglioStileAssoSoftware.xsl",
            "FoglioStileAssoSoftware_v1.1.xsl",
        ),
    )
