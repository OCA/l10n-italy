#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
import datetime
from collections import defaultdict
from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


class AccountPaymentAddMoveLines(models.TransientModel):
    _name = 'wizard.account.payment.add.move.lines'
    _description = 'Add to payment order from due dates tree view'

    def _payment_orders(self):
        active_ids = self._context.get('active_ids')
        result = []
        domain = [('state', '=', 'draft'), ('payment_line_ids', '!=', False)]
        orders = self.env['account.payment.order'].search(domain)
        if active_ids and len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            if lines[0].move_id.company_bank_id and \
                    lines[0].move_id.company_bank_id.id:
                bank_id = lines[0].move_id.company_bank_id.id
            else:
                bank_id = 0
            payment_method_code = lines[0].payment_method.code
            if payment_method_code == 'invoice_financing':
                pmethod = ('payment_method_id.code', '=', 'invoice_financing')
                domain.append(pmethod)
                orders = self.env['account.payment.order'].search(domain)
                porders = list()
                for order in orders:
                    adding = True
                    for line in order.payment_line_ids:
                        if line.move_line_id.move_id.company_bank_id.id:
                            to_match_id = \
                                line.move_line_id.move_id.company_bank_id.id
                            if to_match_id != bank_id:
                                adding = False
                    if adding:
                        porders.append(order)
                orders = porders

        for order in orders:
            display = order.name + ' - ' + order.payment_method_id.name
            result.append((str(order.id), display))
        return result

    payment_orders = fields.Selection(
        string='Ordini di pagamento',
        required=True,
        selection='_payment_orders'
    )

    @api.multi
    def add(self):

        active_ids = self._context.get('active_ids')
        payment_method = self.env['account.payment.method']
        # get payment order
        payment_order_id = int(self.payment_orders)
        # validate
        # check payment method (first line)
        payment_order = self.env['account.payment.order'].\
            browse(payment_order_id)

        if len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                payment_method = line.payment_method
                break

            if payment_method and payment_method.code == 'invoice_financing':
                order = payment_order.read([])[0]
                order.update({'massimale': payment_order.massimale})

            # Check for errors
            self._raise_on_errors(lines, payment_order)

            # Aggiunta linee a distinta
            lines.create_payment_line_from_move_line(payment_order)

            if payment_method and payment_method.code == 'invoice_financing':
                if order['massimale'] == order['bank_invoice_financing_amount']:
                    payment_order.bank_invoice_financing_amount = \
                        payment_order.massimale
            # end if

            # Apertura ordine di pagamento
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.order',
                'res_id': payment_order.id,
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'current',
            }
        # end if
    # end add()

    @api.model
    def _raise_on_errors(self, lines, payment_order):
        busy_lines = list()
        payment_methods = defaultdict(lambda: {'count': 0, 'name': None})
        check_order_payment_method = defaultdict(lambda: {'count': 0,
                                                          'name': None})
        # the payment method of the order is different from
        # the payment method of the lines
        # payment_mode_id versus payment_method.id
        # set payment method id from lines already in
        payment_method_lines = [
            line.move_line_id.payment_method.id for line in
            payment_order.payment_line_ids
        ]
        # set payment method name from lines already in
        payment_method_lines_name = [
            line.move_line_id.payment_method.name for line in
            payment_order.payment_line_ids]
        # to do the match we get only the first because they are equals
        order_payment_method_id = payment_method_lines[0]
        order_payment_method_name = payment_method_lines_name[0]

        for line in lines:

            # Detect lines already assigned to a payment order
            if line.payment_line_ids:
                busy_lines.append(line)
            # end if

            # Check same payment method
            payment_methods[line.payment_method.id]['count'] += 1
            payment_methods[line.payment_method.id]['name'] = \
                line.payment_method.name

            # validate lines against order
            if not line.payment_method.id:
                scadenza = line.move_id.name
                date_format = datetime.datetime(
                    year=line.date_maturity.year,
                    month=line.date_maturity.month,
                    day=line.date_maturity.day,
                )
                date_tz = format_date(
                    self.env, fields.Date.context_today(
                        self, date_format))
                raise UserError('ATTENZIONE!\nMetodo di pagamento non '
                                'impostato nella scadenza {sk} del {dt}.'
                                .format(sk=scadenza, dt=date_tz))
                #
                #
                # check_order_payment_method[line.payment_method.id]['name'] =


                #     'Metodo di pagamento non inserito'
                # check_order_payment_method[line.payment_method.id]['count'] += 1

            if line.payment_method.id and line.payment_method.id != \
                    order_payment_method_id:
                check_order_payment_method[line.payment_method.id]['name'] = \
                    line.payment_method.name
                check_order_payment_method[line.payment_method.id]['count'] += 1
        # end for

        error_busy = len(busy_lines) > 0
        error_method = len(payment_methods) > 1
        error_order_payment_method = len(check_order_payment_method) > 0

        if error_busy or error_method or error_order_payment_method:

            error_msg_busy = ''
            if error_busy:
                error_msg_busy = self._error_msg_busy(busy_lines)
            # end if

            error_msg_method = ''
            if error_method:
                error_msg_method = self._error_msg_method(payment_methods)
            # end if

            error_msg_method_order = ''
            if error_order_payment_method:
                error_msg_method_order = \
                    self._error_msg_method_order(check_order_payment_method,
                                                 order_payment_method_name)
            # end if

            # Separate error messages with two newlines if both error
            # messages should be displayed
            error_msg_busy += (error_busy and error_method and '\n\n\n') or ''

            if error_msg_method_order:
                raise UserError(error_msg_busy + error_msg_method + '\n\n\n' +
                                error_msg_method_order)

            raise UserError(error_msg_busy + error_msg_method)
        # end if
    # end _check_for_errors

    @staticmethod
    def _error_msg_busy(busy_lines):
        msg = 'ATTENZIONE!\nLe seguenti righe' \
              'sono già parte di una distinta:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x.invoice_id.number + '    ' + str(x.date_maturity),
                busy_lines
            )
        )

        return msg
    # end _error_msg_busy

    @staticmethod
    def _error_msg_method(payment_methods):
        msg = 'ATTENZIONE!\nSono state selezionate righe' \
              'con più metodi di pagamento:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x['name'],
                payment_methods.values()
            )
        )

        return msg
    # end _error_msg_method

    @staticmethod
    def _error_msg_method_order(check_order_payment_method,
                                order_payment_method_name):
        if order_payment_method_name:

            msg = 'ATTENZIONE!\nSono state selezionate righe ' \
                  'con metodo di pagamento diverso da quello dell\'ordine ' \
                  'selezionato (' + order_payment_method_name + '):\n\n - '
        else:
            msg = 'ATTENZIONE!\nSono state selezionate righe ' \
                  'con metodo di pagamento diverso da quello dell\'ordine ' \
                  'selezionato:\n\n - '

        msg += '\n - '.join(
            map(
                lambda x: x['name'],
                check_order_payment_method.values()
            )
        )

        return msg
    # end _error_msg_method_order

