# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
import base64
import io
import zipfile


class WizardAccountInvoiceExport(models.TransientModel):
    _name = "wizard.fatturapa.export"

    data = fields.Binary("File", readonly=True)
    name = fields.Char('Filename', size=32)
    mark_as_exported = fields.Boolean('Mark as exported', default=True)

    @api.multi
    def export_zip(self):
        attachments = []
        for att in self.env[self._context['active_model']].browse(
                self._context['active_ids']):
            attachments += [att]

        fp = io.BytesIO()
        zf = zipfile.ZipFile(fp, mode="w")

        for att in attachments:
            zf.writestr(att.datas_fname, base64.b64decode(att.datas))
        zf.close()
        fp.seek(0)
        data = fp.read()
        export_report_name = _('E-Invoices XML')
        if self.name:
            export_report_name = self.name
        attach_vals = {
            'name': export_report_name + '.zip',
            'datas_fname': export_report_name + '.zip',
            'datas': base64.encodestring(data),
        }
        att_id = self.env['ir.attachment'].create(attach_vals)
        model_data_obj = self.env['ir.model.data']
        view_rec = model_data_obj.get_object_reference(
            'base', 'view_attachment_form')
        view_id = view_rec and view_rec[1] or False
        if self.mark_as_exported:
            for attachment in attachments:
                attachment.zip_exported = True
        return {
            'view_type': 'form',
            'name': _("Export E-Invoices"),
            'view_id': [view_id],
            'res_id': att_id.id,
            'view_mode': 'form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'context': self._context,
        }
