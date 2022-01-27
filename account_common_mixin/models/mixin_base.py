#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields
from ..engine.compute_iban import (
    get_company_bank_account, get_counterparty_bank_account
)


class BaseMixin:

    def _counterparty_bank_id_domain(self):
        # Variabile separata per facilitare debug
        domain = [('partner_id', '=', self.partner_id.id)]
        return domain
    # end _counterparty_bank_id_domain

    def _company_bank_id_domain(self):
        # Variabile separata per facilitare debug
        domain = [
            ('partner_id', '=', self.env.user.company_id.partner_id.id),
            ('bank_is_wallet', '=', False)
        ]

        return domain
    # end _company_bank_id_domain

    counterparty_bank_id = fields.Many2one(
        string="Banca d'appoggio",
        comodel_name='res.partner.bank',
        domain=_counterparty_bank_id_domain,
        copy=True,
    )

    company_bank_id = fields.Many2one(
        string='Banca aziendale',
        comodel_name='res.partner.bank',
        domain=_company_bank_id_domain,
        copy=True,
    )

    @api.multi
    def _update_iban(self):

        for doc in self:

            doc: BaseMixin

            # Update company bank and counterparty bank
            doc.company_bank_id = get_company_bank_account(doc)
            doc.counterparty_bank_id = get_counterparty_bank_account(doc)

        # end for
    # end _update_iban

    @api.onchange('company_bank_id')
    def _iban_onchange_company_bank_id(self):

        if not self._must_process_event('_iban_onchange_company_bank_id'):
            self._update_partner_bank_id()
        # end if

    # end _onchange_partner_id

    @api.onchange('counterparty_bank_id')
    def _iban_onchange_counterparty_bank_id(self):

        if not self._must_process_event('_iban_onchange_counterparty_bank_id'):
            self._update_partner_bank_id()
        # end if

    # end _onchange_partner_id

    @api.onchange('company_id')
    def _iban_onchange_company_id(self):

        if not self._must_process_event('_iban_onchange_company_id'):

            # Update IBAN
            self._update_iban()

            # Change the partner bank domain
            domain_filters = self._get_domains()
            return domain_filters

        # end if

    # end _onchange_partner_id

    @api.onchange('partner_id')
    def _iban_onchange_partner_id(self):

        if not self._must_process_event('_iban_onchange_partner_id'):

            # Update IBAN
            self._update_iban()

            # Change the partner bank domain
            domain_filters = self._get_domains()
            return domain_filters

        # end if

    # end _iban_onchange_partner_id

    @api.onchange('payment_term_id')
    def _iban_onchange_payment_term_id(self):

        if not self._must_process_event('_iban_onchange_payment_term_id'):

            # Update IBAN
            self._update_iban()

            # Change the partner bank domain
            domain_filters = self._get_domains()
            return domain_filters

        # end if

    # end _iban_onchange_payment_term_id

    @api.multi
    def _update_partner_bank_id(self):

        for doc in self:

            doc: BaseMixin

            comp_bnk = doc.company_bank_id
            ctpt_bnk = doc.counterparty_bank_id

            # Update partner_bank_id
            invoice_type = doc._get_doc_type()
            if invoice_type in ('out_invoice', 'out_refund') and comp_bnk:
                doc.partner_bank_id = comp_bnk
            elif invoice_type in ('in_invoice', 'in_refund') and ctpt_bnk:
                doc.partner_bank_id = ctpt_bnk
            # end if
        # end for

    # end _update_partner_bank_id

    @api.multi
    def _get_doc_type(self):
        """Must be implemented by subclass"""
        self.ensure_one()
        raise NotImplemented()
    # end _get_doc_type

    def _must_process_event(self, event_name):
        """
            Skip the first "on_chage" event if
            'from_purchase_order_change'is set in context
        """

        ctx = self.env.context
        skipped_flag_name = event_name + 'SKIPPED'

        from_po = ctx.get('from_purchase_order_change')
        first_skipped = ctx.get(skipped_flag_name)

        if from_po and not first_skipped:
            ctx[skipped_flag_name] = True
            return True
        else:
            return False
        # end if
    # end _must_skip_event

    @api.multi
    def _get_domains(self):

        self.ensure_one()

        counterparty_p = self.partner_id
        company_p = self.company_id.partner_id

        # Change the partner bank domain
        domain_filters = {
            'domain': {
                'counterparty_bank_id': [
                    ('partner_id', '=', counterparty_p.parent_id.id or counterparty_p.id)
                ],
                'company_bank_id': [
                    ('partner_id', '=', company_p.id),
                    ('bank_is_wallet', '=', False)
                ],
            },
        }

        return domain_filters
    # end _get_domains

