# Copyright 2024 Sergio Zanchetta (PNLUG APS - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class BaseLanguageInstall(models.TransientModel):
    _inherit = "base.language.install"

    def lang_install(self):
        res = super().lang_install()

        lang = self.env["res.lang"]

        if "it_IT" in self.lang_ids.mapped("code"):
            lang.update_menu_finance_it_translation()

        return res
