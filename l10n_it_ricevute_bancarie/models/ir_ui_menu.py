#  Copyright 2022 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    def write(self, vals):
        old_parent = self.parent_id
        new_parent_id = vals.get("parent_id")

        res = super().write(vals)

        if new_parent_id:
            # Move the RiBa menu if any of
            # its siblings (menu having same parent before write)
            # is moved (parent changes).
            # This happens when account_accountant (enterprise)
            # is installed or uninstalled.
            root_riba_menu = self.env.ref("l10n_it_ricevute_bancarie.menu_riba")
            parent_riba_menu = root_riba_menu.parent_id
            if old_parent == parent_riba_menu and new_parent_id != old_parent.id:
                root_riba_menu.parent_id = new_parent_id
        return res
