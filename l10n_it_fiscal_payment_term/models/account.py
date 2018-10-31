# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FatturapaPaymentTerm(models.Model):
    # _position = ['2.4.1']
    _name = "fatturapa.payment_term"
    _description = 'Fiscal Payment Term'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class FatturapaPaymentMethod(models.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment_method"
    _description = 'Fiscal Payment Method'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


#  used in fatturaPa export
class AccountPaymentTerm(models.Model):
    # _position = ['2.4.2.2']
    _inherit = 'account.payment.term'

    fatturapa_pt_id = fields.Many2one(
        'fatturapa.payment_term', string="Fiscal Payment Term")
    fatturapa_pm_id = fields.Many2one(
        'fatturapa.payment_method', string="Fiscal Payment Method")
