#  Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class Common(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.module = "l10n_it_edi_oss"
