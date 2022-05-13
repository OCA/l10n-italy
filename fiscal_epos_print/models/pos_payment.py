from odoo import fields, models

class PosPayment(models.Model):
    _inherit='pos.payment'

    def _export_for_ui(self, payment):
        res=super(PosPayment, self)._export_for_ui(payment)
        res['fiscalprinter_payment_type'] = payment.payment_method_id.fiscalprinter_payment_type
        res['fiscalprinter_payment_index'] =  payment.payment_method_id.fiscalprinter_payment_index
        return  res
class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

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
