from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon as _FatturaPACommon,
)


class FatturaPACommon(_FatturaPACommon):
    def setUp(self):
        super().setUp()

        def _fix_payability(tax, ref):
            reftax = self.env.ref(ref).sudo()
            tax.payability = reftax.payability

        # XXX - to be moved to l10n_it_fatturapa_out.tests.fatturapa_common ?
        _fix_payability(self.tax_22, "l10n_it_fatturapa.tax_22")
        _fix_payability(self.tax_10, "l10n_it_fatturapa.tax_10")
        _fix_payability(self.tax_22_SP, "l10n_it_fatturapa.tax_22_SP")

        self.fiscal_position_sp = self.env["account.fiscal.position"].create(
            {
                "name": "Split payment",
                "split_payment": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": self.tax_22.id,
                            "tax_dest_id": self.tax_22_SP.id,
                        },
                    )
                ],
            }
        )
        self.company.sp_account_id = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_current_assets").id,
                )
            ],
            limit=1,
        )

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out_sp"
        return super().getAttachment(name, module_name)

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out_sp"
        return super().getFile(filename, module_name)
