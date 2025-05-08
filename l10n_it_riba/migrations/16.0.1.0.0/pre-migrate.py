#  Copyright 2023 Simone Rubino - AionTech
#  Copyright 2024 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

# pylint: disable=odoo-addons-relative-import
# because
#   from ... import hooks
# raises
#   ImportError: attempted relative import with no known parent package
from odoo.addons.l10n_it_riba import hooks


def migrate(cr, installed_version):
    # copy old riba.distinta.line.state refs
    openupgrade.copy_columns(
        cr,
        {"riba_distinta_line": [("state", None, None)]},
    )

    # copy old riba.distinta.state refs
    openupgrade.copy_columns(
        cr,
        {"riba_distinta": [("state", None, None)]},
    )

    # Used by OpenUpgrade when module is in `apriori`
    hooks.migrate_old_module(cr)
