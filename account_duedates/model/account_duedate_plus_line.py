#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero


class DueDateLine(models.Model):
    _name = 'account.duedate_plus.line'
    _description = 'Scadenze collegate ad una fattura/nota di credito'

    _order = 'due_date'

    duedate_manager_id = fields.Many2one(
        comodel_name='account.duedate_plus.manager',
        string='Gestore scadenze',
        requred=True,
        ondelete='cascade',
    )

    due_date = fields.Date('Data di scadenza', requred=True)
    payment_method_id = fields.Many2one(
        comodel_name='account.payment.method',
        string='Metodo di pagamento',
        requred=False  # Non sempre è impostato il metodo di pagamento nei termini di pagamento
    )
    due_amount = fields.Float(string='Importo', required=True)

    move_line_id = fields.One2many(
        comodel_name='account.move.line',
        inverse_name='duedate_line_id',
        string='Riferimento riga registrazione contabile',
    )

    proposed_new_value = fields.Float(string='Importo proposto')

    is_paid = fields.Boolean(string='Pagato', compute='_get_paid')

    schedule_payment = fields.Boolean(string='In pagamento',
                                      compute='_get_scheduled_payment')

    def _get_scheduled_payment(self):
        for line in self:
            rec = self.env['account.payment.line'].search([
                ('move_line_id', 'in', [x.id for x in line.move_line_id])])
            if rec:
                line.schedule_payment = True
            else:
                line.schedule_payment = False

    def _get_paid(self):
        for line in self:
            if line.move_line_id:
                for line_pymnt in line.move_line_id:
                    if line_pymnt.payment_id:
                        line.is_paid = True
            else:
                line.is_paid = False

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):

        # Check if fields are empty
        dd_miss = not values['due_date']
        da_miss = not values['due_amount']

        # If all fields are empty return an empty recordset,
        # otherwise return the newly created record
        if dd_miss or da_miss:
            empty_recordset = self.env['account.duedate_plus.line']
            return empty_recordset.search([])
        else:
            result = super().create(values)
            return result
        # end if
    # end create

    @api.multi
    def write(self, values):

        result = super().write(values)

        if not self.env.context.get('RecStop'):
            if 'due_date' in values:
                for duedate_line in self:
                    duedate_line.with_context(
                        RecStop=True
                    ).update_duedate()
                # end for
            # end for

            if 'payment_method_id' in values:
                for duedate_line in self:
                    duedate_line.with_context(
                        RecStop=True
                    ).update_payment_method()
                # end for
            # end if
        # end if

        return result
    # end write

    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS

    @api.onchange('due_amount')
    def _onchange_due_amount(self):
        '''
        Reset proposed_new_value if it is equal to due_amount
        '''
        precision = self.env.user.company_id.currency_id.rounding
        difference = self.due_amount - self.proposed_new_value

        if float_is_zero(difference, precision_rounding=precision):
            self.proposed_new_value = 0
        # end if
    # end _onchange_due_amount

    # @api.onchange('due_date')
    # def _onchange_due_date(self, values=None):
    #     pass
    #     if not self.due_date and values:
    #         return {
    #             'warning': {
    #                 'title': 'Data scadenza',
    #                 'message': 'La data non può essere vuota'
    #             }
    #         }
    #     end if
    # end _check_due_amount

    # @api.onchange('due_amount')
    # def _onchange_due_amount(self, values=None):
    #     error = self._validate_due_amount(values)
    #     if error and values:
    #         return {'warning': error}
    #     # end if
    # end _check_due_amount

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # CONSTRAINTS - begin

    # @api.constrains('due_date')
    # def _constraint_due_date(self):
    #     if not self.due_date:
    #         raise UserError('La data non può essere vuota')
    #     # end if
    # end _check_due_amount

    # @api.constrains('due_amount')
    # def _constraint_due_amount(self):
    #     error = self._validate_due_amount()
    #     if error:
    #         raise UserError(error['message'])
        # end if
    # end _check_due_amount

    # CONSTRAINTS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # VALIDATION METHODS - begin

    # Validation methods return error message if field is not valid,
    # None otherwise

    # VALIDATION METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # UPDATE MOVE LINE METHODS - begin

    # Update the associated duedate_line
    @api.onchange('date_maturity')
    def update_duedate(self):
        if self.move_line_id:
            self.move_line_id[0].date_maturity = self.due_date
        # end if
    # end _update_duedate

    @api.onchange('payment_method_id')
    def update_payment_method(self):
        if self.move_line_id:
            self.move_line_id[0].payment_method = self.payment_method_id
        # end if
    # end _update_payment_method

    # UPDATE MOVE LINE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

