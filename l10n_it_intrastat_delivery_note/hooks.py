import logging

from odoo import SUPERUSER_ID, api, tools

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    # Convert 'HS Code' to an 'Intrastat code'
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        product_ids = env["product.product"].search([("hs_code", "!=", False)])
        for code, products in tools.groupby(product_ids, lambda x: x.hs_code):
            report_intrastat_code_id = env["report.intrastat.code"].search(
                [("name", "=", code)]
            )
            if not report_intrastat_code_id:
                _logger.warning("No Intrastat Code found for HS Code: '%s'", code)
                continue

            env["product.product"].browse([i.id for i in products]).write(
                {
                    "intrastat_code_id": report_intrastat_code_id.id,
                    "intrastat_type": report_intrastat_code_id.type,
                }
            )


def uninstall_hook(cr, registry):
    # Move every 'Intrastat code' to 'HS Code'
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        if hasattr(env["product.product"], "hs_code"):
            product_ids = env["product.product"].search(
                [("intrastat_code_id", "!=", False), ("hs_code", "=", False)]
            )

            for code, products in tools.groupby(
                product_ids, lambda x: x.intrastat_code_id
            ):
                env["product.product"].browse([i.id for i in products]).write(
                    {"hs_code": code.name}
                )
