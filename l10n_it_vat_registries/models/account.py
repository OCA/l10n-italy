# -*- coding: utf-8 -*-
# Copyright 2011-2013 Associazione OpenERP Italia
# (<http://www.openerp-italia.org>).
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountTax(models.Model):
    _inherit = "account.tax"

    exclude_from_registries = fields.Boolean(
        string='Exclude from VAT registries')
    parent_tax_ids = fields.Many2many(
        'account.tax', 'account_tax_filiation_rel', 'child_tax', 'parent_tax',
        string='Parent Taxes')

    cee_type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase')
    ], string='Include in VAT register',
        help="Use in the case of tax with 'VAT integration'. This "
             "specifies the VAT register (sales / purchases) where the "
             "tax must be computed.")

    def get_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_balance_domain(
            state_list, type_list)
        if self.env.context.get('vat_registry_journal_ids'):
            domain.append((
                'move_id.journal_id', 'in',
                self.env.context['vat_registry_journal_ids']))
        return domain

    def get_base_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_base_balance_domain(
            state_list, type_list)
        if self.env.context.get('vat_registry_journal_ids'):
            domain.append((
                'move_id.journal_id', 'in',
                self.env.context['vat_registry_journal_ids']))
        return domain
