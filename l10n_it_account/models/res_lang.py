# Copyright 2024 Sergio Zanchetta (PNLUG APS - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Lang(models.Model):
    _inherit = "res.lang"

    def toggle_active(self):
        res = super().toggle_active()

        if "it_IT" in [lang.code for lang in self.filtered(lambda L: L.active)]:
            self.update_menu_finance_it_translation()

        return res

    def update_menu_finance_it_translation(self):
        """In Odoo the inheritance mechanism is not yet implemented for menus.
        Changing a menu item name doesn't create a new string to be translated
        but overwrites the source string of the original module to which the menu
        belongs to. This is a workaround that allows the translated string to be
        modified in the same way.
        """
        menu_finance_id = self.env["ir.model.data"]._xmlid_to_res_id(
            "account.menu_finance"
        )
        menu_finance = self.env["ir.ui.menu"].browse(menu_finance_id)

        field_name = menu_finance._fields["name"]
        translations = field_name._get_stored_translations(menu_finance)

        translations["it_IT"] = "Contabilità"
        self.env.cache.update_raw(menu_finance, field_name, [translations], dirty=True)
        menu_finance.modified(["name"])
