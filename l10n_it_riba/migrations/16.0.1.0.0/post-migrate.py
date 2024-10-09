#  Copyright 2023 Simone Rubino - AionTech
#  Copyright 2024 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

NEW_MODULE_NAME = "l10n_it_riba"


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr,
        NEW_MODULE_NAME,
        "migrations/16.0.1.0.0/data/noupdate.xml",
    )

    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name("state"),
        "state",
        [
            ("draft", "draft"),
            ("confirmed", "confirmed"),
            ("accredited", "credited"),
            ("paid", "paid"),
            ("unsolved", "past_due"),
            ("cancel", "cancel"),
        ],
        table="riba_slip_line",
    )

    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name("state"),
        "state",
        [
            ("draft", "draft"),
            ("accepted", "accepted"),
            ("accredited", "credited"),
            ("paid", "paid"),
            ("unsolved", "past_due"),
            ("cancel", "cancel"),
        ],
        table="riba_slip",
    )
