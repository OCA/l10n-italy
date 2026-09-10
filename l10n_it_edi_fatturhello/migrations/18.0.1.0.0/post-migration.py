# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def get_fatturhello_channel_ids(env):
    env.cr.execute(
        """
SELECT id
FROM sdi_channel
WHERE channel_type = 'fatturhello'
        """,
    )
    return env.cr.fetchall()


def removed_channel(env):
    """The ES Channel does not exist anymore.

    Move/remove the data of Fatturhello channels.
    """
    if channel_ids := get_fatturhello_channel_ids(env):
        # Move fields to the Company.
        set_clause = ",\n".join(
            f"{channel_field} = sdi_channel.{channel_field}"
            for channel_field in [
                "fatturhello_base_url",
                "fatturhello_username",
                "fatturhello_login_authtoken",
                "fatturhello_login_authtoken_create_date",
            ]
        )
        openupgrade.logged_query(
            env.cr,
            f"""
UPDATE res_company
SET
    fatturhello_is_used = true,
    {set_clause}
FROM sdi_channel
WHERE
    res_company.sdi_channel_id = sdi_channel.id
    AND sdi_channel.id = ANY(%(channel_ids)s)
        """,
            dict(
                channel_ids=channel_ids,
            ),
        )

        # Remove the mail activities, like "Renew Login".
        openupgrade.logged_query(
            env.cr,
            """
DELETE FROM mail_activity
WHERE
    res_model = 'sdi.channel'
    AND res_id = ANY(%(channel_ids)s)
        """,
            dict(
                channel_ids=channel_ids,
            ),
        )


def removed_attachment(env):
    """The FatturaPA attachment does not exist anymore.

    Move/remove the data of Fatturhello attachments.
    """
    # Fatturhello fields
    set_clause = ",\n".join(
        f"{attachment_field} = fatturapa_attachment_out.{attachment_field}"
        for attachment_field in [
            "fatturhello_protocol",
            "fatturhello_last_processed_status_datetime",
        ]
    )
    openupgrade.logged_query(
        env.cr,
        f"""
UPDATE account_move
SET
    {set_clause}
FROM fatturapa_attachment_out
    JOIN sdi_channel
        ON fatturapa_attachment_out.channel_id = sdi_channel.id
    JOIN ir_attachment
        ON ir_attachment.res_model = 'account.move'
        AND ir_attachment.id = fatturapa_attachment_out.ir_attachment_id
WHERE
    sdi_channel.id = ANY(%(channel_ids)s)
    AND account_move.id = ir_attachment.res_id
    """,
        dict(
            channel_ids=get_fatturhello_channel_ids(env),
        ),
    )

    # State field: this is not managed by other modules
    # because they don't know how to translate it
    openupgrade.logged_query(
        env.cr,
        """
UPDATE account_move
SET
    l10n_it_edi_state = 'sent_to_fatturhello'
WHERE
    fatturapa_state = 'sent_to_fatturhello'
    """,
    )


@openupgrade.migrate()
def migrate(env, version):
    removed_channel(env)
    removed_attachment(env)
