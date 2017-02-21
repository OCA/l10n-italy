# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountRCTypeTax(models.Model):
    _name = 'account.rc.type.tax'
    _description = 'Tax Mapping for self invoices'

    rc_type_id = fields.Many2one(
        'account.rc.type',
        string='RC type',
        required=True,
        ondelete='cascade')
    purchase_tax_id = fields.Many2one(
        'account.tax',
        string='Purchase Tax',
        required=True)
    sale_tax_id = fields.Many2one(
        'account.tax',
        string='Sale Tax',
        required=True)
    _sql_constraints = [
        ('purchase_sale_tax_uniq',
         'unique (rc_type_id,purchase_tax_id,sale_tax_id)',
         'Tax mappings can be defined only once per rc type.')
    ]


class AccountRCType(models.Model):
    _name = 'account.rc.type'
    _description = 'Reverse Charge Type'

    name = fields.Char('Name', required=True)
    method = fields.Selection(
        (('integration', 'VAT Integration'),
            ('selfinvoice', 'Self Invoice')),
        string='Method',
        required=True)
    partner_type = fields.Selection(
        (('supplier', 'Supplier'), ('other', 'Other')),
        string='Self Invoice Partner Type')
    partner_id = fields.Many2one(
        'res.partner',
        string='Self Invoice Partner',
        help="Partner used on RC self invoices.")
    journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Journal',
        help="Journal used on RC self invoices.")
    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Payment Journal',
        help="Journal used to pay RC self invoices.")
    payment_partner_id = fields.Many2one(
        'res.partner',
        string='Self Invoice Payment Partner',
        help="Partner used on RC self invoices.")
    transitory_account_id = fields.Many2one(
        'account.account',
        string='Self Invoice Transitory Account',
        help="Transitory account used on self invoices.")
    tax_ids = fields.One2many(
        'account.rc.type.tax',
        'rc_type_id',
        help="Example: 22_A_I_UE, 22_V_I_UE",
        string='Self Invoice Tax Mapping')
    description = fields.Text('Description')
    invoice_text = fields.Text('Text on Invoice')
    self_invoice_text = fields.Text('Text in Self Invoice')
