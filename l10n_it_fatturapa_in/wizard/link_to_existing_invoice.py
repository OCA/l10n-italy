# -*- coding: utf-8 -*-

from openerp.osv import fields
from openerp.osv import orm
from openerp.tools.translate import _
from openerp.osv.osv import except_osv
from openerp.addons.l10n_it_fatturapa.bindings import fatturapa


class WizardLinkToInvoice(orm.TransientModel):
    _name = "wizard.link.to.invoice"
    _description = "Link to Supplier Invoice"

    _columns = {
        'invoice_id': fields.many2one(
            'account.invoice', string="Invoice", required=True)
        }

    def get_invoice_obj(self, cr, uid, fatturapa_attachment):
        xml_string = self.pool.get('ir.attachment').get_xml_string(
            cr, uid, fatturapa_attachment.ir_attachment_id.id)
        return fatturapa.CreateFromDocument(xml_string)

    def link(self, cr, uid, ids, context={}):
        active_ids = context.get('active_ids')
        if len(active_ids) != 1:
            raise except_osv(
                _('Error'), _("You can select only 1 XML file to link"))
        wizardBrws = self.browse(cr, uid, ids[0], context)
        invoiceObj = self.pool.get('account.invoice')
        invoiceObj.write(cr, uid, [wizardBrws.invoice_id.id], {
            'fatturapa_attachment_in_id': active_ids[0]
            }, context)
        # extract pdf if attached
        fatturapa_attachment_obj = self.pool['fatturapa.attachment.in']
        for fatturapa_attachment_id in active_ids:
            fatturapa_attachment = fatturapa_attachment_obj.browse(
                cr, uid, fatturapa_attachment_id, context=context)
            fatt = self.get_invoice_obj(cr, uid, fatturapa_attachment)
            for FatturaBody in fatt.FatturaElettronicaBody:
                # 2.5
                AttachmentsData = FatturaBody.Allegati
                if AttachmentsData and wizardBrws.invoice_id:
                    fatturapa_attachment_obj.extract_attachments(
                        cr, uid, AttachmentsData, wizardBrws.invoice_id.id)
