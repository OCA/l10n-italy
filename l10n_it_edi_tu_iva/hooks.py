# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    """Cite the Testo Unico IVA in the taxes existing before the installation.

    The taxes of a chart of accounts loaded later are handled by the
    ``account.chart.template`` override.
    """
    env["account.tax"]._l10n_it_tu_iva_update_law_references()
