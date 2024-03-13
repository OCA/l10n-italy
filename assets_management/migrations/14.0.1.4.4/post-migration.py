from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, "assets_management", "migrations/14.0.1.4.4/noupdate_changes.xml"
    )
