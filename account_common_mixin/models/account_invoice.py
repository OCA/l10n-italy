#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models
from .mixin_base import BaseMixin


class AccountInvoice(models.Model, BaseMixin):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        new_invoice: AccountInvoice = super().create(vals)
        company_bank = new_invoice.company_bank_id
        counter_bank = new_invoice.counterparty_bank_id

        if new_invoice.type in ('out_invoice', 'out_refund') and company_bank:
            new_invoice.partner_bank_id = company_bank
        elif new_invoice.type in ('in_invoice', 'in_refund') and counter_bank:
            new_invoice.partner_bank_id = counter_bank
        # end if

        return new_invoice
    # end create

    def write(self, vals):
        if 'company_bank_id' in vals:

            lines = self.move_id.line_ids.filtered(
                lambda
                    x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'company_bank_id': vals['company_bank_id']
            })

            if self.state == 'open':
                self.move_id.write({
                        'company_bank_id': vals['company_bank_id'],
                })
            # end if
            if self.state == 'draft':
                self.write({
                    'partner_bank_id': vals['company_bank_id'],
                })
            # end if

        # end if
        if 'counterparty_bank_id' in vals:

            lines = self.move_id.line_ids.filtered(
                lambda
                    x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'counterparty_bank_id': vals[
                    'counterparty_bank_id']
            })

            if self.state == 'open':
                self.move_id.write({
                        'counterparty_bank_id': vals['counterparty_bank_id'],
                })
            # end if
            if self.state == 'draft':
                self.write({
                    'partner_bank_id': vals['counterparty_bank_id'],
                })
            # end if
        # end if
        return super().write(vals)
    # end write

    # Extend method that loads invoice data from PO
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        """Copy values from a Purchase Order to the new invoice form"""

        # Save the Purchase Order reference since the superclass
        # method will delete it once completed
        po = self.purchase_id

        # Call superclass function
        res = super().purchase_order_change()

        # Copy bank accounts related infos from Purchase Order object
        if po:
            self.company_bank_id = po.company_bank_id and po.company_bank_id
            self.counterparty_bank_id = po.counterparty_bank_id and po.counterparty_bank_id
        # end if

        # Return the result
        return res

    # end purchase_order_change

    @api.multi
    def adapt_document(self):
        self.ensure_one()
        adapt_data = {
            'model': 'account.invoice',
            'type':  self.type,
            'fatturapa_pm_id': None,
            'payment_mode_id': None,
            'assigned_bank': None,
            'assigned_income_bank': None,
            'default_company_bank': None,
            'default_counterparty_bank': None
        }

        if self.payment_term_id and self.payment_term_id.fatturapa_pm_id:
            adapt_data['fatturapa_pm_id'] = self.payment_term_id.fatturapa_pm_id
        # end if

        if self.payment_mode_id:
            adapt_data['payment_mode_id'] = self.payment_mode_id
        # end if

        if self.company_id and self.company_id.partner_id:
            pbk = self.company_id.partner_id
            bank = self.env['res.partner.bank']
            # python 3.7
            if pbk.bank_ids:
                for bk in pbk.bank_ids:
                    bank = bk
                    break
                # end for
            # end if
            adapt_data['default_company_bank'] = bank
        # end if

        # Update with counterparty data
        counterparty_bank_infos = (
            self.partner_id and self.partner_id.bank_infos()
            or
            {}
        )
        adapt_data.update(counterparty_bank_infos)

        return adapt_data
    # end adapt_document

    @api.multi
    def _get_doc_type(self):
        self.ensure_one()
        return self.type
    # end _get_doc_type

