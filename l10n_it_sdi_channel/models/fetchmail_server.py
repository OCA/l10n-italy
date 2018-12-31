# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from osv import fields, osv 
from tools.translate import _


class FetchmailServer(osv.osv):
    _inherit = "fetchmail.server"

    _columns = {
        'is_fatturapa_pec': fields.boolean('FatturaPA PEC server'),
    }
FetchmailServer()
