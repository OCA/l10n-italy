# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(
        env.cr,
        [
            ("faturapa.activity.progress", "fatturapa.activity.progress"),
            ("faturapa.summary.data", "fatturapa.summary.data"),
        ],
    )
    openupgrade.rename_tables(
        env.cr,
        [
            ("faturapa_activity_progress", "fatturapa_activity_progress"),
            ("faturapa_summary_data", "fatturapa_summary_data"),
        ],
    )
