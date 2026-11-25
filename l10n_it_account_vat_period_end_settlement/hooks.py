# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

from odoo.addons.l10n_it_account.migration_tools import EXISTING_TAX_MAX_ID_PARAM

_logger = logging.getLogger(__name__)


def post_absorb_old_module(env):
    """Exclude the old taxes that were not part of the VAT settlements.

    Up to 16.0 a tax was included in the VAT settlements only when it was linked
    to a ``vat_statement_account_id``; in 18.0 the information is carried by the
    inverted ``exclude_from_vat_settlements`` flag.

    The 18.0 chart taxes have no ``vat_statement_account_id`` (the column is a
    leftover), so the update is restricted to the taxes that existed before the
    18.0 chart records were created, when ``l10n_it_account`` recorded their
    highest id in an ir.config_parameter. The marker is always consumed, also
    when there is nothing to migrate, so it cannot leak into a later upgrade.
    """
    icp = env["ir.config_parameter"].sudo()
    existing_max_id = icp.get_param(EXISTING_TAX_MAX_ID_PARAM)
    icp.search([("key", "=", EXISTING_TAX_MAX_ID_PARAM)]).unlink()
    if not openupgrade.column_exists(env.cr, "account_tax", "vat_statement_account_id"):
        return
    query = """
        UPDATE account_tax SET exclude_from_vat_settlements = True
        WHERE vat_statement_account_id IS NULL
    """
    params = ()
    if existing_max_id:
        query += " AND id <= %s"
        params = (int(existing_max_id),)
    else:
        # No 18.0 chart records were created by l10n_it_account: keep the
        # pre-existing behaviour and exclude every tax without the account.
        _logger.warning(
            "No %s marker found: every tax without a vat_statement_account_id "
            "is excluded from the VAT settlements",
            EXISTING_TAX_MAX_ID_PARAM,
        )
    # Push pending ORM writes before the raw UPDATE, otherwise a later flush
    # would overwrite it.
    env["account.tax"].flush_model(["exclude_from_vat_settlements"])
    openupgrade.logged_query(env.cr, query, params)
    Tax = env["account.tax"]
    Tax.invalidate_model(["exclude_from_vat_settlements"])


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "account_vat_period_end_statement"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "account_vat_period_end_statement",
                    "l10n_it_account_vat_period_end_settlement",
                ),
            ],
            merge_modules=True,
        )
