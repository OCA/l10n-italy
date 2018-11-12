# -*- coding: utf-8 -*-

from openerp.osv import fields
from openerp.osv import orm
from openerp.tools.translate import _
from openerp.osv.osv import except_osv


class WizardLinkToInvoice(orm.TransientModel):
    _name = "wizard.link.to.invoice"
    _description = "Link to Supplier Invoice"
    
    _columns = {
        'invoice_id': fields.many2one(
            'account.invoice', string="Invoice", required=True)
        }

    def link(self, cr, uid, ids, context={}):
        active_ids = context.get('active_ids')
        if len(active_ids) != 1:
            raise except_osv(_('Error' ),
                             _("You can select only 1 XML file to link"))
        wizardBrws = self.browse(cr, uid, ids[0], context)
        invoiceObj = self.pool.get('account.invoice')
        invoiceObj.write(cr, uid, [wizardBrws.invoice_id.id], {
            'fatturapa_attachment_in_id': active_ids[0]
            }, context)
