# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from osv import fields, osv
from tools.translate import _


class IrMailServer(osv.osv):
    _inherit = "email.server"

    _columns = {
        'is_fatturapa_pec': fields.boolean('FatturaPA PEC server'),
        'email_from_for_fattura_pa': fields.char('Sender Email Address', size=250),
    }
IrMailServer()
