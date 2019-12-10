# coding=utf-8

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    fiscalprinter_payment_type = fields.Selection(
        [
            ('0', 'Cash'),
            ('1', 'Cheque'),
            ('2', 'Credit/Credit Card'),
            ('3', 'Ticket')
        ],
        'Payment type',
        help='The payment type to send to the Fiscal Printer.',
        default='0'
    )

    fiscalprinter_payment_index = fields.Integer(
        string='Credit Card/Ticket Index',
        help='Set the index of the given payment type to specify the detail. '
             'Such index of the payment type must programmed on the fiscal '
             'printer')
