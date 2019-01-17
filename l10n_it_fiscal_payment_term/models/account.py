# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Gianmarco Conte - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models
from openerp.tools.translate import _


class FatturapaPaymentTerm(models.Model):
    # _position = ['2.4.1']
    _name = "fatturapa.payment_term"
    _description = 'Fiscal Payment Term'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


#  used in fatturaPa export
class AccountPaymentTerm(models.Model):
    # _position = ['2.4.2.2']
    _inherit = 'account.payment.term'

    fatturapa_pt_id = fields.Many2one(
        'fatturapa.payment_term',
        string=_('Fiscal Payment Term'),
        required=True
    )
