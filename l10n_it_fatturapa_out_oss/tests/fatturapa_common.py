from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon as _FatturaPACommon,
)


class FatturaPACommon(_FatturaPACommon):
    def setUp(self):
        super().setUp()

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out_oss"
        return super().getAttachment(name, module_name)

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out_oss"
        return super().getFile(filename, module_name)
