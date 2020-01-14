from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    printer_ip = fields.Char(
        'Printer IP Address',
        help='The hostname or IP address of the fiscal printer',
        size=45
    )
    use_https = fields.Boolean(
        string='Use https',
        default=False,
    )
    show_receipt_when_printing = fields.Boolean(
        string='Show receipt on screen when printing', default=True)
    fiscal_printer_serial = fields.Char(string='Fiscal Printer Serial')

    fiscal_cashdrawer = fields.Boolean(string='Fiscal Printer Open CashDrawer')
