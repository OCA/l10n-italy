# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


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
    with_supplier_self_invoice = fields.Boolean(
        "With additional supplier self invoice",
        help="Flag this to enable the creation of an additional supplier self"
             " invoice. This is tipically used for extraUE suppliers, "
             "in order to show, in supplier register, an invoice to the "
             "specified partner (tipically, my company), instead of the "
             "extraUE partner")
    partner_id = fields.Many2one(
        'res.partner',
        string='Self Invoice Partner',
        help="Partner used on RC self invoices.")
    journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Journal',
        help="Journal used on RC self invoices.")
    supplier_journal_id = fields.Many2one(
        'account.journal',
        string='Supplier Self Invoice Journal',
        help="Journal used on RC supplier self invoices.")
    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Payment Journal',
        help="Journal used to pay RC self invoices.")
    transitory_account_id = fields.Many2one(
        'account.account',
        string='Self Invoice Transitory Account',
        help="Transitory account used on self invoices.")
    tax_ids = fields.One2many(
        'account.rc.type.tax',
        'rc_type_id',
        help="Example: 22_A_I_UE, 22_V_I_UE",
        string='Self Invoice Tax Mapping',
        copy=False)
    description = fields.Text('Description')
    self_invoice_text = fields.Text('Text in Self Invoice')

    @api.multi
    @api.constrains('with_supplier_self_invoice', 'tax_ids')
    def _check_tax_ids(self):
        for rctype in self:
            if rctype.with_supplier_self_invoice and len(rctype.tax_ids) > 1:
                raise ValidationError(_(
                    'When "With additional supplier self invoice" you must set'
                    ' only one tax mapping line: only 1 tax per invoice is '
                    'supported'
                ))
