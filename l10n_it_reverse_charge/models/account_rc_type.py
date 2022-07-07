# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2022 Simone Rubino - TAKOBI

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountRCTypeTax(models.Model):
    _name = 'account.rc.type.tax'
    _description = 'Tax Mapping for self invoices'

    rc_type_id = fields.Many2one(
        'account.rc.type',
        string='RC type',
        required=True,
        ondelete='cascade')
    original_purchase_tax_id = fields.Many2one(
        'account.tax',
        string='Original Purchase Tax',
        required=False)
    purchase_tax_id = fields.Many2one(
        'account.tax',
        string='Purchase Tax',
        required=True)
    sale_tax_id = fields.Many2one(
        'account.tax',
        string='Sale Tax',
        required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', related='rc_type_id.company_id',
        store=True)
    _sql_constraints = [
        ('purchase_sale_tax_uniq',
         'unique (rc_type_id,purchase_tax_id,sale_tax_id)',
         'Tax mappings from Purchase Tax to Sale Tax '
         'can be defined only once per Reverse Charge Type.'),
        ('original_purchase_sale_tax_uniq',
         'unique (rc_type_id,'
         'original_purchase_tax_id,purchase_tax_id,sale_tax_id)',
         'Tax mappings from Original Purchase Tax to Purchase Tax to Sale Tax '
         'can be defined only once per Reverse Charge Type.'),
    ]

    @api.constrains(
        'original_purchase_tax_id',
        'rc_type_id',
    )
    def _constrain_supplier_self_invoice_mapping(self):
        for mapping in self:
            rc_type = mapping.rc_type_id
            if rc_type.with_supplier_self_invoice:
                if not mapping.original_purchase_tax_id:
                    raise ValidationError(
                        _("Original Purchase Tax is required "
                          "for Reverse Charge Type {rc_type_name} having "
                          "With additional supplier self invoice enabled")
                        .format(
                            rc_type_name=rc_type.display_name,
                        )
                    )


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
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.constrains(
        'with_supplier_self_invoice',
        'tax_ids',
    )
    def _constrain_with_supplier_self_invoice(self):
        with_supplier_types = self.filtered('with_supplier_self_invoice')
        if with_supplier_types:
            with_supplier_types.mapped('tax_ids') \
                ._constrain_supplier_self_invoice_mapping()

    def map_tax(self, taxes, key_tax_field, value_tax_field):
        """
        Map each tax in `taxes`, based on the mapping defined by `self.tax_ids`.

        Raise an exception if a mapping is not found for some of `taxes`.

        :param key_tax_field: Field of the mapping lines
            to be used as key for searching the tax
        :param value_tax_field: Field of the mapping lines
            to be used as value for mapping the tax
        :param taxes: Taxes to be mapped
        """
        self.ensure_one()
        mapped_taxes = self.env['account.tax'].browse()
        for tax in taxes:
            for tax_mapping in self.tax_ids:
                if tax_mapping[key_tax_field] == tax:
                    mapped_taxes |= tax_mapping[value_tax_field]
                    break
            else:
                # Tax not found in mapping
                raise UserError(
                    _("Can't find tax mapping for {tax_name} "
                      "in Reverse Charge Type {rc_type_name}, "
                      "please check the configuration.")
                    .format(
                        tax_name=tax.display_name,
                        rc_type_name=self.display_name,
                    )
                )
        return mapped_taxes
