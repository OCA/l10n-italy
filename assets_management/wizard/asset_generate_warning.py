from odoo import fields, models


class AssetGenerateWarning(models.TransientModel):
    _name = "asset.generate.warning"

    wizard_id = fields.Many2one(
        "wizard.asset.generate.depreciation", string="Asset Wizard"
    )
    reason_lines = fields.One2many(
        comodel_name="asset.confirm.reason.line",
        inverse_name="confirm_id",
        string="Elenco",
    )

    def do_generate(self):
        return self.wizard_id.do_generate()

    # end do_generate


class AssetConfirmReasonLine(models.TransientModel):
    _name = "asset.confirm.reason.line"

    confirm_id = fields.Many2one("asset.generate.warning", string="Numero elenco")
    reason = fields.Char(string="Avviso", size=255, readonly=True)
