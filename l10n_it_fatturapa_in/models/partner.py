#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    e_invoice_default_product_id = fields.Many2one(
        comodel_name="product.product",
        string="E-bill Default Product",
        help="Used by electronic invoice XML import. "
        "If filled in, generated bill lines will use this product when "
        "no other possible product is found.",
    )
    e_invoice_detail_level = fields.Selection(
        [
            ("0", "Minimum"),
            ("1", "Tax Rate"),
            ("2", "Maximum"),
        ],
        string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
        "User will have to create them, according to what specified in "
        "the electronic bill.\n"
        "Tax rate level: Rate level: an invoice line is created for each "
        "rate present in the electronic invoice\n"
        "Maximum level: every line contained in the electronic bill "
        "will create a line in the bill.",
        default="2",
        required=True,
    )
    e_invoice_price_decimal_digits = fields.Integer(
        "E-bills prices decimal digits",
        help="Decimal digits used in prices computation. This is needed to correctly "
        "import e-invoices with many decimal digits, not being forced to "
        "increase decimal digits of all your prices. "
        'Otherwise, increase "Product Price" precision. '
        "-1 to use the default precision",
        default=-1,
    )
    e_invoice_quantity_decimal_digits = fields.Integer(
        "E-bills quantities decimal digits",
        help='Decimal digits used for quantity field. See "prices decimal digits". '
        "-1 to use the default precision",
        default=-1,
    )
    e_invoice_discount_decimal_digits = fields.Integer(
        "E-bills discounts decimal digits",
        help='Decimal digits used for discount field. See "prices decimal digits". '
        "-1 to use the default precision",
        default=-1,
    )

    # https://github.com/odoo/odoo/pull/71920
    # this is temporary fix, we depend on the issue do the solved for our test
    # to be all green
    def _split_vat(self, vat):
        vat = vat.replace(" ", "")
        return super()._split_vat(vat)

    @api.constrains("vat", "country_id")
    def check_vat(self):
        if "fatturapa_in_skip_no_it_vat_check" in self.env.context:
            # Replicate e-invoice specifications check on IdFiscaleIVA:
            # only italian VAT is checked
            italy = self.env.ref("base.it")
            it_partners = self.filtered(lambda p: p.country_id == italy)
            super(Partner, it_partners).check_vat()
            try:
                super(Partner, self - it_partners).check_vat()
            except ValidationError as ve:
                log_message = (
                    "Validation Error skipped during e-bill import:\n"
                    "{exc_message}".format(
                        exc_message=ve.args[0],
                    )
                )
                _logger.info(log_message)
        else:
            super().check_vat()
