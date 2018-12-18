# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - FatturaPA - Emission - PEC Support
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

from openerp.osv import orm


class SendPEC(orm.TransientModel):
    _name = 'wizard.fatturapa.send.pec'
    _description = "Wizard to send multiple e-invoice PEC"

    def send_pec(self, cr, uid, ids, context=None):
        if context and context.get('active_ids'):
            self.pol.get('fatturapa.attachment.out').send_via_pec(
                cr, uid, context['active_ids'], context=context)
