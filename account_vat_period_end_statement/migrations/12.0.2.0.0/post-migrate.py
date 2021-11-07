from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.m2o_to_x2m(
        env.cr, env["date.range"], "date_range",
        "vat_statement_ids", "vat_statement_id")
