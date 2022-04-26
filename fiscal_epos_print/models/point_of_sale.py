#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models, exceptions


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

    @api.constrains('printer_ip', 'iface_reprint_done_order')
    def _check_fiscal_epos_reprint(self):
        """If an order has been printed by the fiscal printer,
        the core reprint functionality has to be avoided
        because it would create another fiscal document.
        """
        for config in self:
            if config.printer_ip and config.iface_reprint_done_order:
                raise exceptions.ValidationError(
                    _("Reprint cannot be done for a fiscal printer yet.\n"
                      "Please disable 'Reprint Orders' "
                      "or unset 'Printer IP Address'.")
                )
