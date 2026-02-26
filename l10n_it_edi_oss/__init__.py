from . import models
from . import wizard

OSS_EXEMPT_REASON = "N3.2"
OSS_LAW_REFERENCE = "Art. 41 D.L. 331/1993"


def _l10n_it_edi_oss_post_init_hook(env):
    oss_taxes = env["account.tax"].search(
        [
            ("oss_country_id", "!=", False),
            ("company_id.account_fiscal_country_id.code", "=", "IT"),
            "|",
            ("l10n_it_exempt_reason", "=", False),
            ("l10n_it_exempt_reason", "!=", OSS_EXEMPT_REASON),
        ]
    )
    if oss_taxes:
        oss_taxes.write(
            {
                "l10n_it_exempt_reason": OSS_EXEMPT_REASON,
                "l10n_it_law_reference": OSS_LAW_REFERENCE,
            }
        )
