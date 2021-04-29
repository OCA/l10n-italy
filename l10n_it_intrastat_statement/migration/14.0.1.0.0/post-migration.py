from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr,
        "l10n_it_intrastat_statement",
        "migrations/14.0.1.0.0/noupdate_changes.xml",
    )
