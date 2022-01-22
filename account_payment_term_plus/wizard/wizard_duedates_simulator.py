# Copyright (c) 2020
#
# Copyright 2022 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardDuedatesSimulator(models.TransientModel):
    _name = 'wizard.duedates.simulator'
    _description = 'Simulatore scadenze'

    date_due = fields.Date(
        string='Data di decorrenza',
        default=fields.Date.today,
        required=True
    )
    amount_untaxed = fields.Float(
        string='Imponibile',
        default=0.0,
        required=True
    )
    amount_total = fields.Float(
        string='Importo',
        default=0.0,
        required=True
    )

    duedates_lines = fields.One2many(
        comodel_name='wizard.duedate.line',
        inverse_name='simulator_id',
        string='Scadenze',
    )

    @api.multi
    def simulate(self):
        active_id = self._context.get('active_id')
        self._validate_form()
        payment_term_model = self.env['account.payment.term'].browse(active_id)
        date = self.date_due
        add_tax = False
        if payment_term_model.first_duedate_tax:
            amount = self.amount_untaxed
            tax = self.amount_total - self.amount_untaxed
            add_tax = True
        else:
            amount = self.amount_total
            tax = 0.0
        duedates = payment_term_model.compute(amount, date)

        for duedate in duedates:
            for line in duedate:
                ddue = line[0]

                if add_tax:
                    damount = line[1] + tax
                    add_tax = False
                else:
                    damount = line[1]

                vals = {
                    'due_date': ddue,
                    'due_amount': damount,
                    'simulator_id': self.id,
                }
                self.env['wizard.duedate.line'].create(vals)

        view_name = 'account_payment_term_plus.wizard_duedates_simulator_result'
        return {
            'name': 'Simulatore',
            'view_mode': 'form',
            'view_id': self.env.ref(view_name).id,
            'view_type': 'form',
            'res_model': 'wizard.duedates.simulator',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def _validate_form(self):
        if not self.date_due:
            raise UserError('La data di decorrenza deve essere impostata')

        if self.amount_total <= 0:
            raise UserError('L\'importo deve essere maggiore di zero')

        if self.amount_untaxed <= 0:
            raise UserError('L\'imponibile deve essere maggiore di zero')

        if self.amount_untaxed > self.amount_total:
            raise UserError('L\'importo deve essere maggiore dell\'imponibile')

        return True

    @api.onchange('amount_total')
    def onchange_amount_total(self):
        if self.amount_total > 0:
            self.amount_untaxed = (self.amount_total / 122) * 100


class WizardDueDateLine(models.TransientModel):
    _name = 'wizard.duedate.line'
    _description = 'Linea Scadenze'

    _order = 'due_date'

    due_date = fields.Date(string='Data di scadenza')
    due_amount = fields.Float(string='Importo')
    simulator_id = fields.Many2one(
        string="Simulatore",
        comodel_name="wizard.duedates.simulator",
    )
