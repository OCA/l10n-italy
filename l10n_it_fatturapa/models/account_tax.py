# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class AccountTax(models.Model):
    _inherit = 'account.tax'
    non_taxable_nature = fields.Selection([
        ('N1', 'escluse ex art. 15'),
        ('N2', 'non soggette'),
        ('N3', 'non imponibili'),
        ('N4', 'esenti'),
        ('N5', 'regime del margine'),
        ('N6', 'inversione contabile (reverse charge)'),
        ], string="Non taxable nature")
    payability = fields.Selection([
        ('I', 'Immediate payability'),
        ('D', 'Deferred payability'),
        ('S', 'Split payment'),
        ], string="VAT payability")
    law_reference = fields.Char(
        'Law reference', size=128)

    @api.model
    def get_tax_by_invoice_tax(self, invoice_tax):
        if ' - ' in invoice_tax:
            tax_descr = invoice_tax.split(' - ')[0]
            tax_ids = self.search([
                ('description', '=', tax_descr),
                ])
            if not tax_ids:
                raise UserError(
                    _('No tax %s found') % tax_descr)
            if len(tax_ids) > 1:
                raise UserError(
                    _('Too many tax %s found') % tax_descr)
        else:
            tax_name = invoice_tax
            tax_ids = self.search([
                ('name', '=', tax_name),
                ])
            if not tax_ids:
                raise UserError(
                    _('No tax %s found') % tax_name)
            if len(tax_ids) > 1:
                raise UserError(
                    _('Too many tax %s found') % tax_name)
        return tax_ids[0]
