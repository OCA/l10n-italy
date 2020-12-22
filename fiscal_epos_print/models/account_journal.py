from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    fiscalprinter_payment_type = fields.Selection(
        [
            ('0', 'Cash'),
            ('1', 'Cheque'),
            ('2', 'Credit or Credit Card'),
            ('3', 'Ticket'),
            ('4', 'Ticket with number'),
            ('5', 'No Paid'),
            ('6', 'Discount on payment'),
        ],
        'Payment type',
        help='The payment type to send to the Fiscal Printer.',
        default='0'
    )

    fiscalprinter_payment_index = fields.Integer(
        string='Electronic Payment / Ticket Index',
        help='Set the index of the given payment type to specify the detail.')
