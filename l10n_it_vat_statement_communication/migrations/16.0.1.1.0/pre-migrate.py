import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return

    rm_old_vat_communication_multi_company_rule(env)


def rm_old_vat_communication_multi_company_rule(env):
    _logger.info(
        "Migration of l10n_it_vat_statement_communication - search for"
        " previous multi company rule for 'comunicazione.liquidazione' model"
    )
    module = "l10n_it_vat_statement_communication"
    rule_xml_id = "comunucazione_liquidazione_iva_multi_company"
    old_vat_comm_multi_company_rule_ref = env.ref(
        f"{module}.{rule_xml_id}", raise_if_not_found=False
    )

    if not old_vat_comm_multi_company_rule_ref:
        # avoid unlink not existent record
        _logger.warning(
            "Migration of l10n_it_vat_statement_communication - previous"
            " multi company rule for 'comunicazione.liquidazione' model not"
            " found"
        )
        return

    _logger.info(
        "Migration of l10n_it_vat_statement_communication - unlink"
        " previous multi company rule for 'comunicazione.liquidazione' model"
    )
    old_vat_comm_multi_company_rule_ref.unlink()
