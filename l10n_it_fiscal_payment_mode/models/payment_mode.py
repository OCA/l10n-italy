# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################

from openerp import fields, models
from openerp.tools.translate import _


#  used in fatturaPa export
class PaymentMode(models.Model):
    # _position = ['2.4.2.2']
    _inherit = 'payment.mode'

    fatturapa_pm_id = fields.Many2one(
        comodel_name='fatturapa.payment_method',
        string=_('Fiscal Payment Method'),
        required=True
    )
