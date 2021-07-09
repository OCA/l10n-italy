from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    printer_ip = fields.Char(
        'Printer IP Address',
        help='The hostname or ip address of the hardware printer, '
        'please fill this field if you want use you receipts printer',
        size=45
    )
    use_https = fields.Boolean(
        string='Use https',
        default=False,
    )
