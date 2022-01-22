#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from datetime import timedelta


from odoo import models, api, fields
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError

LIMIT_DAYS = 60


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    duedate_manager_id = fields.One2many(
        string='Gestore scadenze',
        comodel_name='account.duedate_plus.manager',
        inverse_name='invoice_id',
    )

    duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        related='duedate_manager_id.duedate_line_ids',
        readonly=False
    )

    no_delete_duedate_line_ids = fields.One2many(
        string='Righe scadenze',
        comodel_name='account.duedate_plus.line',
        related='duedate_manager_id.duedate_line_ids',
        readonly=False
    )

    check_duedates_payment = fields.Boolean(string='Ha pagamenti',
                                            compute='checks_payment')

    duedates_amount_current = fields.Monetary(
        string='Ammontare scadenze',
        compute='_compute_duedates_amounts'
    )

    duedates_amount_unassigned = fields.Monetary(
        string='Ammontare non assegnato a scadenze',
        compute='_compute_duedates_amounts'
    )

    date_effective = fields.Date(
        string='Data di decorrenza',
        states={"draft": [("readonly", False)]},
        readonly=True,
        default='',
        copy=False,
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        new_invoice: AccountInvoice = super().create(values)

        # Set default for date_effective
        new_invoice._default_date_effective()

        # Return the result of the write command
        return new_invoice
    # end create

    @api.multi
    def write(self, values):

        result = super().write(values)

        # Set default values, but avoid the "infinite
        # recursive calls to write" issue
        if not self.env.context.get('StopRecursion'):

            # Set context variable to stop recursion
            self = self.with_context(StopRecursion=True)

            for invoice in self:

                if invoice.state == 'open':
                    # check validation (amount and dates)
                    ret = invoice.duedate_manager_id.validate_duedates()
                    if ret:
                        msg = ret['title'] + '\n' + ret['message']
                        raise UserError(msg)
                    if 'duedate_line_ids' in values and invoice.move_id and \
                            invoice.check_duedates_payment is False:

                        # riporta la move in bozza
                        invoice.move_id.button_cancel()

                        # aggiorna le scadenze e i movimenti
                        invoice.move_id.write_credit_debit_move_lines()

                        # riporta in stato confermato la move
                        invoice.move_id.post()
                    # end if

                    if 'company_bank_id' in values:
                        lines = invoice.move_id.line_ids.filtered(
                            lambda
                                x: x.reconciled is False and x.payment_order.id is False
                        )

                        lines.write({
                            'company_bank_id': values['company_bank_id']
                        })
                    # end if

                    if 'counterparty_bank_id' in values:
                        lines = invoice.move_id.line_ids.filtered(
                            lambda
                                x: x.reconciled is False and x.payment_order.id is False
                        )

                        lines.write({
                            'counterparty_bank_id': values[
                                'counterparty_bank_id']
                        })
                    # end if

                elif invoice.state == 'draft':
                    # Set default value for date_effective if user did not
                    # supplied a value. This operation is performed only if
                    # the invoice is in state draft since invoices in other
                    # states does NOT allow changing dates.
                    if not invoice.date_effective:
                        invoice._default_date_effective()
                # end if

                if 'invoice_line_ids' in values:
                    invoice.update_duedates()
                # end if

            # end for

        # end if "StopRecursion"

        return result
    # end write

    def post(self):
        result = super().post()
        return result
    # end post

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            if not invoice.date_effective:
                invoice.date_effective = invoice.date_invoice
            # end if
        # end for
        return super().invoice_validate()
    # end invoice_validate

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PUBLIC METHODS - begin

    @api.multi
    def action_update_duedates_and_move_lines(self):
        # Update account.duedate_plus.line records
        for invoice in self:
            invoice.update_duedates()
        # end for
    # end update_duedates_and_move_lines

    @api.multi
    def action_move_create(self):

        super().action_move_create()

        for inv in self:

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Copia dati da testata fattura

            updates = dict()

            if inv.move_id.type is False:
                updates['type'] = self.type
            # end if

            # Data fattura
            updates['invoice_date'] = inv.date_invoice

            # Data decorrenza
            if inv.date_effective:
                updates['date_effective'] = inv.date_effective
            else:
                updates['date_effective'] = inv.date_invoice

            # Termini di pagamento
            pt = inv.payment_term_id
            updates['payment_term_id'] = pt and pt.id or False

            # Update the "move"
            inv.move_id.write(updates)
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # Update the DueManager adding the reference to the "account.move"
            inv.duedate_manager_id.write({'move_id': inv.move_id.id})

        # end for

        return True
    # end action_move_create

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):

        self.ensure_one()
        self._ensure_duedate_manager()
        move_lines = super().finalize_invoice_move_lines(move_lines)

        move_lines_model = self.env['account.move.line']
        # Linee di testata che rappresentano le scadenze da RIMPIAZZARE
        head_lines = [
            ml
            for ml in move_lines
            # if (ml[2]['tax_ids'] is False and ml[2]['tax_line_id'] is False)
            if move_lines_model.get_line_type(
                ml[2], duedate_mode=True) in ('receivable', 'payable')
        ]

        # may be empty if account_total is zero
        if len(head_lines) == 0:
            return move_lines

        # Altre linee che vanno MANTENUTE
        new_lines = [
            ml
            for ml in move_lines
            if move_lines_model.get_line_type(
                ml[2], duedate_mode=True
            ) not in ('receivable', 'payable')
        ]

        prototype_line = head_lines[0][2]

        if not self.duedate_manager_id.duedate_line_ids:
            self.duedate_manager_id.write_duedate_lines()

        if self.amount_total == 0.0 and \
                not self.duedate_manager_id.duedate_line_ids:
            return move_lines

        tax_pm_lines = []

        tax_pm_id = self.env['account.payment.method'].search(
            [('code', '=', 'tax')])

        for duedate in self.duedate_manager_id.duedate_line_ids:

            # Create the new line
            new_line_dict = prototype_line.copy()

            # Update - maturity date
            new_line_dict['date_maturity'] = duedate.due_date

            # Update - reference to the duedate line
            new_line_dict['duedate_line_id'] = duedate.id

            # Update - set amount
            if new_line_dict['credit']:
                new_line_dict['credit'] = duedate.due_amount
            elif new_line_dict['debit']:
                new_line_dict['debit'] = duedate.due_amount
            else:
                pass
            # end if

            # Update - payment method
            new_line_dict['payment_method'] = duedate.payment_method_id.id

            if duedate.payment_method_id.id == tax_pm_id.id:
                tax_pm_lines.append(
                    (0, 0, new_line_dict)
                )
            else:
                new_lines.append(
                    (0, 0, new_line_dict)
                )
        # end for

        return tax_pm_lines + new_lines
    # end finalize_invoice_move_lines

    @api.multi
    def update_duedates(self):
        for inv in self:

            # Ensure duedate_manager is configured
            inv._get_duedate_manager()

            # Generate duedates
            duedate_line_list = inv.duedate_manager_id.generate_duedate_lines()

            # Generate the commands list for the ORM update method
            updates_list = list()

            # Remove old records
            if inv.duedate_line_ids:
                updates_list += [(2, duedate_line.id, 0) for duedate_line in inv.duedate_line_ids]
            # end if

            # Create new records
            if duedate_line_list:
                updates_list += [(0, 0, duedate_line) for duedate_line in duedate_line_list]
            # end if

            # Update the record
            if updates_list:
                inv.update({'duedate_line_ids': updates_list})
            # end if
    # end update_duedates

    def checks_payment(self):
        for invoice in self:
            invoice.check_duedates_payment = False
            for line in invoice.duedate_line_ids:
                rec = invoice.env['account.payment.line'].search([
                    ('move_line_id', 'in', [x.id for x in line.move_line_id])])
                if rec:
                    invoice.check_duedates_payment = True
                # end if
            # end for
    # end checks_payment

    @api.multi
    def action_invoice_cancel(self):
        if self.check_duedates_payment:
            raise UserError('Attenzione!\nNon è possibile effettuare '
                            'l\'annullamento perchè alcune scadenze sono '
                            'state inserite in una distinta.')
        return super().action_invoice_cancel()

    # PUBLIC METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS - begin

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        if not self.invoice_line_ids:
            return
        # end if
        super()._onchange_invoice_line_ids()
        self.update_duedates()
    # end _onchange_invoice_line_ids

    @api.onchange('duedate_line_ids')
    def _onchange_duedate_line_ids(self):
        self._compute_duedates_amounts()
    # end _onchange_duedate_line_ids

    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        self.update_duedates()
    # end _onchange_payment_term_id

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        self._update_date_effective()
    # end _onchange_date_invoice

    @api.onchange('date')
    def _onchange_date(self):
        self._update_date_effective()
        return super()._onchange_date()
    # end _onchange_date_invoice

    @api.onchange('duedates_amount_unassigned')
    def _onchange_duedates_amount_unassigned(self):
        '''
        Reset proposed_new_value if duedates_amount_unassigned is zero
        '''
        precision = self.env.user.company_id.currency_id.rounding

        if float_is_zero(
                self.duedates_amount_unassigned, precision_rounding=precision):
            for line in self.duedate_line_ids:
                line.proposed_new_value = 0
            # end for
        # end if
    # end _onchange_duedates_amount_unassigned

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):

        if self.date_effective:
            date_invoice = self.date_effective
        else:
            date_invoice = self.date_invoice
        # end if

        if not date_invoice:
            date_invoice = fields.Date.context_today(self)
        # end if

        if self.payment_term_id:
            pterm = self.payment_term_id
            pterm_list = pterm.with_context(
                currency_id=self.company_id.currency_id.id).compute(
                value=1, date_ref=date_invoice)[0]
            self.date_due = max(line[0] for line in pterm_list)
        elif self.date_due and (date_invoice > self.date_due):
            self.date_due = date_invoice
        # end if
    # end _onchange_payment_term_date_invoice

    @api.onchange('date_effective')
    def _onchange_date_effective(self):
        date_invoice = False
        if self.date_effective:
            date_invoice = self.date_effective
        elif self.date_invoice:
            date_invoice = self.date_invoice
        if date_invoice:
            # check if the date is inside limits + - 60 days
            throw_warning = self._check_limit_date(date_invoice)
            if self.payment_term_id:
                pterm = self.payment_term_id
                pterm_list = pterm.with_context(
                    currency_id=self.company_id.currency_id.id).compute(
                    value=1, date_ref=date_invoice)[0]
                self.date_due = max(line[0] for line in pterm_list)
            elif self.date_due and (date_invoice > self.date_due):
                self.date_due = date_invoice
            self.update_duedates()
            if throw_warning:
                return {
                    'warning': {
                        'title': 'Attenzione!',
                        'message': 'Data di decorrenza fuori '
                                   'limiti (+60 -60 giorni).'}
                }
    # end _onchange_date_effective

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROTECTED METHODS - begin

    @api.model
    def _check_limit_date(self, date):
        if self.date_invoice:
            upper_limit_date = self.date_invoice + timedelta(days=LIMIT_DAYS)
            lower_limit_date = self.date_invoice - timedelta(days=LIMIT_DAYS)
            if date:
                return not (lower_limit_date < date < upper_limit_date)
            # end if
        # end if
        return False
    # end _check_limit_date

    @api.model
    def _get_duedate_manager(self):
        '''
        Return the duedates manager for this invoice
        :return: The duedates manager object for the invoice
                 (account.duedate_plus.manager)
        '''

        # Check if duedate manager is missing
        duedate_mgr_miss = not self.duedate_manager_id

        # Add the Duedate Manager if it's missing
        if duedate_mgr_miss:
            self._create_duedate_manager()
        # end if

        # Return the manager
        return self.duedate_manager_id
    # end get_duedate_manager

    @api.model
    def _create_duedate_manager(self):
        # Add the Duedates Manager
        duedate_manager = self.env['account.duedate_plus.manager'].create({
            'invoice_id': self.id
        })

        self.update({'duedate_manager_id': duedate_manager})
    # end _create_duedate_manager

    @api.model
    def _ensure_duedate_manager(self):
        # check if duedate_amanger is missing

        if not self.duedate_manager_id.id:
            duedate_manager = self.env['account.duedate_plus.manager'].create({
                'invoice_id': self.id
            })
            self.write({'duedate_manager_id': duedate_manager})
        # end if

    # end _create_duedate_manager

    @api.multi
    @api.depends('duedate_line_ids', 'amount_total')
    def _compute_duedates_amounts(self):

        for inv in self:
            # Somma ammontare di ciascuna scadenza
            lines_total = sum(
                # Estrazione ammontare da ciascuna scadenza
                map(lambda l: l.due_amount, inv.duedate_line_ids)
            )

            # Aggiornamento campo ammontare scadenze
            inv.duedates_amount_current = lines_total

            # Aggiornamento campo ammontare non assegnato a scadenze
            inv.duedates_amount_unassigned = inv.amount_total - lines_total
        # end for
    # end _compute_duedate_lines_amount

    @api.model
    def _default_date_effective(self):
        if not self.date_effective:
            self.date_effective = self.date_invoice
        # end if
    # end _default_date_effective

    @api.model
    def _update_date_effective(self):
        """
        Gestione delle regole relative alla data di decorrenza (date_effective)
        :return:
        """

        # TODO: rivedere con Antonio!!!!

        # Incoming document flag
        doc_in = self.type in ('in_invoice', 'in_refund')

        # Difference between date_invoice and date in days,
        # if any of the two dates is not set return 0 as difference
        dates_set = self.date_invoice and self.date
        diff_days = dates_set and abs(self.date_invoice - self.date).days or 0

        # Decide which rule to apply
        if doc_in and diff_days > 15:

            # Documento ricevuto (inbound)
            # Regola [2b] - se le due date data fattura e data registrazione
            # differiscono per più di 15 gg allora:
            #  - date decorrenza assume il valore della data di registrazione
            #  - vengono ricalcolate le scadenze
            self.date_effective = self.date

        else:

            # Regola [1f]
            self.date_effective = self.date_invoice

        # end if

        # Update duedates
        self.update_duedates()

    # end _update_date_effective

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
