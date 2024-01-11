from openupgradelib import openupgrade

_delete_xmlids = ["l10n_it_ricevute_bancarie.riba_config_company_rule"]


@openupgrade.migrate()
def migrate(env, version):

    openupgrade.load_data(
        env.cr,
        "l10n_it_ricevute_bancarie",
        "migrations/14.0.1.8.2/noupdate_changes.xml",
    )
    openupgrade.delete_records_safely_by_xml_id(env, _delete_xmlids)
