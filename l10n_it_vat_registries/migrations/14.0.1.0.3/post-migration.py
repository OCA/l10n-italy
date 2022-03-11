#  Copyright 2022 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Update report with migration because it is a 'no-update' record
    report = env.ref("l10n_it_vat_registries.action_report_registro_iva")
    report.unlink_action()
