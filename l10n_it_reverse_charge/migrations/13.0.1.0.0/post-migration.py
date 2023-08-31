#  Copyright 2021 Simone Vanin - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_reverse_charge", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )
