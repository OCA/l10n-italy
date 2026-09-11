# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_edi_extension.tests.common import Common as ExtensionCommon


class Common(ExtensionCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_td29"
