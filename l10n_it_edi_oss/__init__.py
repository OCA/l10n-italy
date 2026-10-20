from . import models
from .hooks import pre_absorb_old_module


def _l10n_it_edi_oss_post_init_hook(env):
    from .constants import OSS_EXEMPT_REASON, OSS_LAW_REFERENCE

    oss_tag = env.ref("l10n_eu_oss.tag_oss", raise_if_not_found=False)
    if not oss_tag:
        return

    oss_taxes = env["account.tax"].search(
        [
            ("invoice_repartition_line_ids.tag_ids", "in", oss_tag.ids),
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
