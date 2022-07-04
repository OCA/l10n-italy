from openupgradelib.openupgrade import rename_xmlids


def migrate(cr, version):

    rename_xmlids(
        cr,
        [
            (
                "l10n_it_sdi_channel.sdi_pec_first_address",
                "l10n_it_fatturapa_pec.sdi_pec_first_address",
            ),
            (
                "l10n_it_sdi_channel.sdi_channel_pec",
                "l10n_it_fatturapa_pec.sdi_channel_pec",
            ),
        ],
    )
