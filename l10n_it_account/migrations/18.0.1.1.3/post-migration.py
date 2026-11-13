# Copyright 2026 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

from odoo.tools import float_compare, parse_version

from odoo.addons.l10n_it_account.migration_tools import EXISTING_TAX_MAX_ID_PARAM

_logger = logging.getLogger(__name__)

# Chart template models whose existing records are linked to the
# ``account.<company_id>_<xmlid>`` external ids used by the 18.0 chart.
# ``account.account`` is only linked (never created): the new taxes/tax groups
# reference the standard accounts by template xmlid.
LINK_MODELS = ("account.account", "account.tax.group", "account.tax")
# Chart template models whose missing records are created.
# Tax groups must be loaded before taxes because the taxes reference them.
CREATE_MODELS = ("account.tax.group", "account.tax")
# Version of l10n_it_account_vat_period_end_settlement whose migration script
# consumes the EXISTING_TAX_MAX_ID_PARAM marker.
VAT_SETTLEMENT_VERSION = "18.0.1.0.7"


def _get_l10n_it_companies(env):
    return env["res.company"].search([("chart_template", "=", "it")])


def _store_existing_tax_max_id(env):
    """Tell the VAT settlement module which taxes existed before the chart load.

    It must be written once, before any 18.0 chart record is created, otherwise
    the settlement migration would exclude the new taxes from the VAT
    settlements. It is written only when the settlement migration is going to
    run (module installed and version below the one owning the script), so that
    an unconsumed marker cannot be picked up by a later upgrade.
    """
    settlement_modules = (
        "account_vat_period_end_statement",
        "l10n_it_account_vat_period_end_settlement",
    )
    Module = env["ir.module.module"].sudo()
    settlement = Module
    for name in settlement_modules:
        settlement |= Module.search([("name", "=", name)], limit=1)
    settlement = settlement.filtered(
        lambda module: openupgrade.is_module_installed(env.cr, module.name)
    )
    if not settlement:
        return
    installed_versions = [
        parse_version(module.latest_version or "0") for module in settlement
    ]
    if max(installed_versions) >= parse_version(VAT_SETTLEMENT_VERSION):
        return
    env.cr.execute("SELECT COALESCE(MAX(id), 0) FROM account_tax")
    existing_max_id = env.cr.fetchone()[0]
    env["ir.config_parameter"].sudo().set_param(
        EXISTING_TAX_MAX_ID_PARAM, str(existing_max_id)
    )
    _logger.info(
        "Recorded tax id %s as the highest one before the 18.0 chart load",
        existing_max_id,
    )


def _assign_chart_xmlids(env, company, chart_template, template_data):
    """Link the existing chart records to the 18.0 template xmlids.

    In databases migrated from 14.0 the standard Italian taxes, accounts and
    fiscal positions are stored with ``l10n_it.<company_id>_<xmlid>`` external ids
    (e.g. ``l10n_it.1_22v``) while tax groups use ``l10n_it.<xmlid>`` (e.g.
    ``l10n_it.tax_group_iva_22``); the 18.0 chart expects
    ``account.<company_id>_<xmlid>``. Without this step the records would not be
    recognized as already existing and would be created again, as duplicates, by
    the code below (and the tax references to accounts/tax groups would not
    resolve). The old external id is kept and the ``account.`` one is added,
    like the ``l10n_it_account_xmlid_fix`` module does before reloading the chart.
    """
    IrModelData = env["ir.model.data"]
    for model in LINK_MODELS:
        model_records = env[model].with_context(active_test=False)
        for xmlid in template_data.get(model) or {}:
            if chart_template.ref(xmlid, raise_if_not_found=False):
                continue
            company_xmlid = IrModelData.search(
                [
                    ("model", "=", model),
                    ("name", "in", [f"{company.id}_{xmlid}", xmlid]),
                ],
                limit=1,
            )
            if not company_xmlid or company_xmlid.module == "account":
                continue
            record = model_records.browse(company_xmlid.res_id)
            if not record.exists():
                continue
            if model == "account.account":
                # accounts are shared between the companies of a branch
                if company not in record.company_ids:
                    continue
            elif (
                "company_id" in record._fields
                and record.company_id
                and record.company_id != company
            ):
                continue
            _logger.info(
                f"Updated xmlids of {record} with account.{company.id}_{xmlid}"
            )
            IrModelData._update_xmlids(
                [
                    {
                        "xml_id": f"account.{company.id}_{xmlid}",
                        "record": record,
                        "noupdate": True,
                    }
                ]
            )


def _free_tax_names(env, company, missing_taxes):
    """Prefix the taxes whose name clashes with a new one ("[old] ...").

    ``account.tax`` requires a unique (company, name, type_tax_use, tax_scope,
    country) tuple, while the 18.0 chart adds taxes named like the ones users
    create by hand (e.g. the custom "22% SP" tax of ``l10n_it_split_payment`` vs
    the new "22% SP" group tax). Like the chart reload does, the existing tax is
    renamed instead of failing the whole load; posted entries keep pointing to
    it, so historical data is not affected.
    """
    Tax = env["account.tax"]
    country = company.account_fiscal_country_id
    # Default active_test=True, like the search of account.tax._constrains_name:
    # archived taxes do not raise the unique-name constraint.
    for values in missing_taxes.values():
        name = values.get("name")
        type_tax_use = values.get("type_tax_use")
        if not name or not type_tax_use or type_tax_use == "none":
            continue
        domain = [
            ("company_id", "child_of", company.root_id.id),
            ("name", "=", name),
            ("type_tax_use", "=", type_tax_use),
            ("tax_scope", "=", values.get("tax_scope", False)),
            ("country_id", "=", country.id),
        ]
        for tax in Tax.search(domain):
            index = 0
            while Tax.search_count(
                [
                    ("company_id", "child_of", company.root_id.id),
                    ("name", "=", f"[old{index or ''}] {tax.name}"),
                    ("type_tax_use", "=", tax.type_tax_use),
                ]
            ):
                index += 1
            new_name = f"[old{index or ''}] {tax.name}"
            _logger.warning(
                "Tax %s (%s, %s) is renamed to '%s' to make room for the "
                "18.0 chart tax with the same name",
                tax.display_name,
                tax.company_id.display_name,
                tax.type_tax_use,
                new_name,
            )
            tax.name = new_name


def _create_missing_l10n_it_template_records(env):
    """Create the chart template records added by 18.0 and missing in the database.

    The Italian chart template (``l10n_it/data/template``) is only loaded when the
    chart of accounts is installed (or reloaded), so a database migrated from an
    older version misses the records added in 18.0: the N6.x reverse charge taxes,
    the ``0% EU S`` tax, the 2%/12%/20%/21% tax groups, etc. They are required by
    the 18.0 VAT reports and by the e-invoice / VAT settlement modules.

    Only the missing records are loaded (matched by chart template xmlid): the
    existing ones are left untouched, so user customizations of amounts, accounts
    and repartition lines are preserved. This is the programmatic equivalent of
    "reload the chart template", restricted to new records; it relies on the
    (private) ``_get_chart_template_data`` / ``_load_data`` / ``_load_translations``
    chart template API. ``_post_load_data`` is deliberately not called: it only
    sets company/journal defaults that already exist on the migrated company.

    Note: a tax that a migrated database deliberately deleted but that is still
    part of the 18.0 chart is created again by this script.
    """
    chart_template_model = env["account.chart.template"]
    companies = _get_l10n_it_companies(env)
    if not companies:
        _logger.info("No company with the 'it' chart template found")
    for company in companies:
        chart_template = chart_template_model.with_company(company)
        try:
            template_data = chart_template._get_chart_template_data(
                company.chart_template
            )
        except Exception:
            _logger.exception(
                "Unable to read the '%s' chart template data for company %s",
                company.chart_template,
                company.display_name,
            )
            continue
        _assign_chart_xmlids(env, company, chart_template, template_data)
        missing_data = {}
        for model in CREATE_MODELS:
            model_data = template_data.get(model) or {}
            missing_data[model] = {
                xmlid: values
                for xmlid, values in model_data.items()
                if not chart_template.ref(xmlid, raise_if_not_found=False)
            }
        if not any(missing_data.values()):
            continue
        _free_tax_names(env, company, missing_data.get("account.tax") or {})
        company_env = env(
            context=dict(
                env.context,
                allowed_company_ids=[company.id],
                default_company_id=company.id,
                lang="en_US",
                chart_template_load=True,
            )
        )
        # The load is compliance-critical: if it fails, the upgrade must fail
        # too, otherwise the database would silently keep an incomplete tax set.
        with env.cr.savepoint():
            company_env["account.chart.template"]._load_data(
                missing_data, ignore_duplicates=True
            )
            try:
                with env.cr.savepoint():
                    company_env["account.chart.template"]._load_translations(
                        companies=company, template_data=missing_data
                    )
            except Exception:
                # Names/descriptions stay in English: not worth failing the load.
                _logger.exception(
                    "Unable to load the 18.0 chart template translations "
                    "for company %s",
                    company.display_name,
                )
        _logger.info(
            "Company %s: created %s taxes and %s tax groups missing from the "
            "18.0 l10n_it chart",
            company.display_name,
            len(missing_data["account.tax"]),
            len(missing_data["account.tax.group"]),
        )


def _get_split_payment_tax(tax, cache):
    """Return the 18.0 split payment group tax matching ``tax``.

    In 18.0 split payment is detected through the VE38 tags
    (``account.tax._l10n_it_is_split_payment``) and the chart provides a group
    tax ("22% SP", ...) whose positive and negative children carry those tags.
    """
    key = (tax.company_id.id, tax.type_tax_use, round(tax.amount, 2))
    if key not in cache:
        candidates = (
            tax.env["account.tax"]
            .with_context(active_test=False)
            .search(
                [
                    ("company_id", "=", tax.company_id.id),
                    ("type_tax_use", "=", tax.type_tax_use),
                    ("amount_type", "=", "group"),
                ]
            )
        )
        matches = candidates.filtered(
            lambda candidate: any(
                float_compare(child.amount, tax.amount, precision_digits=2) == 0
                and child._l10n_it_is_split_payment()
                for child in candidate.children_tax_ids
            )
        )
        # Prefer the active one, then the lowest sequence/id, so that the result
        # does not depend on the search order.
        if len(matches) > 1:
            _logger.warning(
                "Several 18.0 split payment taxes found for %s%% %s: %s",
                tax.amount,
                tax.type_tax_use,
                matches.mapped("display_name"),
            )
        cache[key] = matches.sorted(lambda t: (not t.active, t.sequence, t.id))[:1]
    return cache[key]


def _migrate_split_payment_fiscal_positions(env):
    """Move the split payment fiscal positions to the 18.0 split payment taxes.

    Up to 16.0 split payment was provided by the OCA module
    ``l10n_it_split_payment``: the fiscal positions flagged with ``split_payment``
    mapped the sale taxes to the company split payment taxes ("22% SP", ...),
    plain percentage taxes. In 18.0 split payment is core: the fiscal position
    must map to the "X% SP" group tax of the chart, otherwise the VAT registries
    and the e-invoice XML do not apply the split payment at all.

    The old module is removed by this migration, so the flag is read from the
    leftover column before Odoo gets rid of it.
    """
    if not openupgrade.column_exists(
        env.cr, "account_fiscal_position", "split_payment"
    ):
        _logger.info(
            "No 'split_payment' column on account_fiscal_position: "
            "nothing to migrate for split payment"
        )
        return
    env.cr.execute("SELECT id FROM account_fiscal_position WHERE split_payment")
    position_ids = [row[0] for row in env.cr.fetchall()]
    if not position_ids:
        _logger.info("No split payment fiscal position found")
        return
    lines = env["account.fiscal.position.tax"].search(
        [
            ("position_id", "in", position_ids),
            ("tax_dest_id", "!=", False),
            ("tax_dest_id.type_tax_use", "=", "sale"),
        ]
    )
    cache = {}
    migrated = 0
    for line in lines:
        old_tax = line.tax_dest_id
        if old_tax.amount_type == "group":
            continue
        new_tax = _get_split_payment_tax(old_tax, cache)
        if not new_tax:
            _logger.warning(
                "Split payment fiscal position %s: no 18.0 split payment tax "
                "found for %s (%s%%), tax mapping left unchanged",
                line.position_id.display_name,
                old_tax.display_name,
                old_tax.amount,
            )
            continue
        line.tax_dest_id = new_tax
        _logger.info(
            f"Updated split payment fiscal position tax line "
            f"{line.position_id.display_name} with old_tax {old_tax.display_name} "
            f"with new tax {new_tax.display_name}",
        )
        migrated += 1
    _logger.info(
        "Split payment: migrated %s fiscal position tax mappings to the "
        "18.0 split payment taxes",
        migrated,
    )


@openupgrade.migrate()
def migrate(env, version):
    _store_existing_tax_max_id(env)
    _create_missing_l10n_it_template_records(env)
    _migrate_split_payment_fiscal_positions(env)
