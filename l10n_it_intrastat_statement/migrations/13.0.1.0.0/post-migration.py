from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_intrastat_statement", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )
