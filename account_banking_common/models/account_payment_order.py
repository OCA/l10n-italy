#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    payment_method_code = fields.Char(
        string='Codice metodo di pagamento',
        related='payment_method_id.code',
    )

    is_wallet_company_bank = fields.Boolean(
        string='Conto di portafoglio aziendale',
        related='company_partner_bank_id.bank_is_wallet',
    )

    @api.multi
    def action_accreditato(self):

        for order in self:
            if order.state == 'uploaded':
                # validation
                if order.payment_method_code not in [
                    'riba_cbi', 'sepa_direct_debit'
                ]:
                    raise UserError('Attenzione!\nIl metodo di pagamento non '
                                    'permette l\'accreditamento.')

                # apertura wizard
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Accreditamento',
                    'res_model': 'wizard.payment.order.credit',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref(
                        'account_banking_common.wizard_payment_order_credit').id,
                    'target': 'new',
                    'res_id': False,
                    "binding_model_id": "account.model_account_payment_order"
                }

    @api.multi
    def registra_accredito(self):
        # The payment method of the selected lines
        raise UserError(
            f'Procedura di registrazione accredito non definita '
            f'per il metodo di pagamento {self.payment_mode_id.name}'
        )
    # end registra_accredito

    @api.multi
    def registra_accredito_standard(self):

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for payment_order in self:

            cfg = payment_order.get_move_config()

            # validazione conti impostati

            if not cfg['sezionale'].id:
                raise UserError("Attenzione!\nSezionale non "
                                "impostato.")

            if not cfg['effetti_allo_sconto'].id:
                raise UserError("Attenzione!\nConto effetti allo sconto "
                                "non impostato.")

            if not cfg['bank_journal'].id:
                raise UserError("Attenzione!\nConto di costo non impostato.")

            # bank_account = cfg['bank_journal'].default_credit_account_id

            lines = self.env['account.payment.line'].search(
                [('order_id', '=', payment_order.id)])

            for line in lines:

                # per ogni riga
                # genero una registrazione

                line_ids = []

                # se ci sono spese le aggiungo
                if amount_expense > 0:

                    credit_account = self.set_expense_credit_account(
                        cfg['bank_journal'])

                    expense_move_line = {
                        'account_id': account_expense_id,
                        'credit': 0,
                        'debit': amount_expense,
                    }
                    line_ids.append((0, 0, expense_move_line))

                    bank_expense_line = {
                        'account_id': credit_account.id,
                        'credit': amount_expense,
                        'debit': 0,
                    }
                    line_ids.append((0, 0, bank_expense_line))
                # end if

                # conto effetti allo sconto
                effetti_allo_sconto = {
                    'account_id': cfg['effetti_allo_sconto'].id,
                    'credit': 0,
                    'debit': line.amount_currency,
                }
                line_ids.append((0, 0, effetti_allo_sconto))

                effetti_attivi = {
                    'account_id': cfg['conto_effetti_attivi'].id,
                    'partner_id': line.partner_id.id,
                    'credit': line.amount_currency,
                    'debit': 0
                }
                line_ids.append((0, 0, effetti_attivi))

                vals = self.env['account.move'].default_get([
                    # 'date_apply_balance',
                    'date_effective',
                    'fiscalyear_id',
                    'invoice_date',
                    'narration',
                    'payment_term_id',
                    'reverse_date',
                    'tax_type_domain',
                ])
                vals.update({
                    'date': fields.Date.today(),
                    'date_apply_vat': fields.Date.today(),
                    'journal_id': cfg['sezionale'].id,
                    'type': 'entry',
                    'ref': "Accreditamento ",
                    'state': 'draft',
                    'line_ids': line_ids,
                    'payment_order_id': payment_order.id
                })

                # Creazione registrazione contabile
                self.env['account.move'].create(vals)

            payment_order.action_done()
    # end registra_accredito_standard

    @api.multi
    def unlink(self):
        
        for order in self:
            if order.state != 'cancel':
                raise UserError(
                    f'L\'ordine di pagamento {order.name} non può essere'
                    f'eliminato perché non è nello stato "Annullato"'
                )
            # end if
        # end for
        
        return super(AccountPaymentOrder, self).unlink()
    # end unlink

    @api.model
    def get_move_config(self):
        '''Returns the journals and accounts to be used for creating new account.move records'''

        po = self
        pay_mode = po.payment_mode_id

        # 1 - Get default config from journal

        cfg = po.journal_id.get_payment_method_config()

        # 2 - Get overrides from payment mode
        if pay_mode.offsetting_account == 'transfer_account':
            assert pay_mode.transfer_journal_id.id
            cfg['transfer_journal'] = pay_mode.transfer_journal_id
            cfg['sezionale'] = cfg['transfer_journal']

            assert pay_mode.transfer_account_id.id
            cfg['transfer_account'] = pay_mode.transfer_account_id
            cfg['conto_effetti_attivi'] = cfg['transfer_account']
            cfg['effetti_allo_sconto'] = cfg['transfer_account']
        # end if

        # 3 - Add bank journal
        cfg['bank_journal'] = po.journal_id

        return cfg
    # end get_move_config

    @api.model
    def set_expense_credit_account(self, journal):

        if journal.is_wallet:
            main_journal = journal.main_bank_account_id
            credit_account = main_journal.default_credit_account_id
        else:
            credit_account = journal.default_credit_account_id
        # end if

        return credit_account
    # end _set_expense_credit_account

    @api.multi
    def _create_reconcile_move(self, hashcode, blines):
        self.ensure_one()
        post_move = self.payment_mode_id.post_move
        am_obj = self.env['account.move']
        mvals = self._prepare_move(blines)
        move = am_obj.create(mvals)
        is_wallet = self.company_partner_bank_id.bank_is_wallet
        if is_wallet:
            move.invoice_date = move.date
            move.date = fields.Date.today()
        blines.reconcile_payment_lines()
        if post_move:
            move.post()
    # end _create_reconcile_move

    @api.multi
    def _prepare_move(self, bank_lines=None):
        vals = super()._prepare_move(bank_lines)

        if self.payment_mode_id.offsetting_account == 'bank_account':
            account = self.journal_id.default_debit_account_id
        elif self.payment_mode_id.offsetting_account == 'transfer_account':
            account = self.payment_mode_id.transfer_account_id

        if account.user_type_id.type not in ('payable', 'receivable'):
            return vals
        else:
            vals['line_ids'] = []
            for bline in bank_lines:
                partner_ml_vals = self._prepare_move_line_partner_account(bline)
                vals['line_ids'].append((0, 0, partner_ml_vals))
                trf_ml_vals = self._prepare_move_line_single_offsetting_account(
                    bline)
                vals['line_ids'].append((0, 0, trf_ml_vals))
        return vals

    @api.multi
    def _prepare_move_line_single_offsetting_account(self, bank_line):
        vals = {}
        if self.payment_type == 'outbound':
            name = _('Payment order %s') % self.name
        else:
            name = _('Debit order %s') % self.name
        if self.payment_mode_id.offsetting_account == 'bank_account':
            vals.update({'date': bank_line.date})
        else:
            vals.update({'date_maturity': bank_line.date})

        if self.payment_mode_id.offsetting_account == 'bank_account':
            account_id = self.journal_id.default_debit_account_id.id
        elif self.payment_mode_id.offsetting_account == 'transfer_account':
            account_id = self.payment_mode_id.transfer_account_id.id
        partner_id = bank_line.payment_line_ids[0].partner_id.id
        vals.update({
            'name': name,
            'partner_id': partner_id,
            'account_id': account_id,
            'credit': (self.payment_type == 'outbound' and
                       bank_line.amount_company_currency or 0.0),
            'debit': (self.payment_type == 'inbound' and
                      bank_line.amount_company_currency or 0.0),
        })
        if bank_line.currency_id != bank_line.company_currency_id:
            sign = self.payment_type == 'outbound' and -1 or 1
            vals.update({
                'currency_id': bank_line.currency_id.id,
                'amount_currency': bank_line.amount_currency * sign,
                })
        return vals

