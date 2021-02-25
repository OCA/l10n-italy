#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ResPartner (models.Model):
    _inherit = 'res.partner'

    epos_print_fiscalcode_receipt = fields.Boolean(
        string="Fiscal code in receipts",
        help="Print fiscal code in receipts for this partner."
    )

    @api.model
    def create_from_ui(self, partner):
        if 'epos_print_fiscalcode_receipt' in partner:
            epos_print_fiscalcode_receipt = \
                partner['epos_print_fiscalcode_receipt'] == 'true'
            partner['epos_print_fiscalcode_receipt'] = \
                epos_print_fiscalcode_receipt
            partner['electronic_invoice_obliged_subject'] = \
                epos_print_fiscalcode_receipt
        return super(ResPartner, self).create_from_ui(partner)
