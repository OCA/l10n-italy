# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from . import models


from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_delivery_note_customer_code"):
        return

    openupgrade.update_module_names(
        cr,
        [
            (
                "l10n_it_delivery_note_customer_code",
                "l10n_it_product_supplierinfo_for_customer_delivery_note",
            ),
        ],
        merge_modules=True,
    )
