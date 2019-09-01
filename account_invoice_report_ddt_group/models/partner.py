# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    ddt_invoice_print_shipping_address = fields.Boolean(
        string='TD shipping address on invoice', default=False,
        help="Show shipping address of TD in invoice report")
