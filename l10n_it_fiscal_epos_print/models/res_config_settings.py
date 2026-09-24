from odoo import fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    printer_ip = fields.Char(related="pos_config_id.printer_ip", readonly=False)
    use_https = fields.Boolean(related="pos_config_id.use_https", readonly=False)
    show_receipt_when_printing = fields.Boolean(
        related="pos_config_id.show_receipt_when_printing", readonly=False
    )
    fiscal_printer_serial = fields.Char(
        related="pos_config_id.fiscal_printer_serial", readonly=False
    )
    fiscal_cashdrawer = fields.Boolean(
        related="pos_config_id.fiscal_cashdrawer", readonly=False
    )
