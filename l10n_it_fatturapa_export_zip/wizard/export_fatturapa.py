# -*- coding: utf-8 -*-

import base64
import io
import zipfile
from datetime import datetime
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class WizardAccountInvoiceExport(models.TransientModel):
    _name = "wizard.fatturapa.export"
    _description = 'Wizard e-invoice export ZIP'

    @api.model
    def _default_name(self):
        return "%s_%s" % (
            _("E-invoice-export"), datetime.now().strftime('%Y%m%d%H%M'))

    data = fields.Binary("File", readonly=True)
    name = fields.Char('Filename', default=_default_name, required=True)

    @api.multi
    def export_zip(self):
        self.ensure_one()
        attachments = self.env[self.env.context['active_model']].browse(
            self.env.context['active_ids'])
        for att in attachments:
            if att.exported_zip:
                raise UserError(_(
                    "Attachment %s already exported. Remove ZIP file first"
                ) % att.display_name)
            if not att.datas or not att.datas_fname:
                raise UserError(
                    _("Attachment %s does not have XML file")
                    % att.display_name)

        fp = io.BytesIO()
        with zipfile.ZipFile(fp, mode="w") as zf:
            for att in attachments:
                zf.writestr(att.datas_fname, base64.b64decode(att.datas))
        fp.seek(0)
        data = fp.read()
        attach_vals = {
            'name': self.name + '.zip',
            'datas_fname': self.name + '.zip',
            'datas': base64.encodestring(data),
        }
        zip_att = self.env['ir.attachment'].create(attach_vals)
        for att in attachments:
            att.exported_zip = zip_att
        return {
            'view_type': 'form',
            'name': _("Export E-Invoices"),
            'res_id': zip_att.id,
            'view_mode': 'form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
        }
