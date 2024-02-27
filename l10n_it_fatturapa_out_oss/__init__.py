from . import wizard
from odoo import api, SUPERUSER_ID


def _l10n_it_fatturapa_out_oss_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    oss_taxes = env["account.tax"].search([("oss_country_id", "!=", False)])
    oss_taxes.write(
        {
            "kind_id": env.ref("l10n_it_account_tax_kind.n3_2").id,
            "law_reference": "Art. 41 D.L. 331/1993",
        }
    )
