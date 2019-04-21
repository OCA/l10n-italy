# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, exceptions


class ComunicazioneLiquidazioneExportFile(models.TransientModel):
    _name = "comunicazione.liquidazione.export.file"
    _description = "Export file xml della comunicazione della liquidazione IVA"

    file_export = fields.Binary('File', readonly=True)
    name = fields.Char('File Name', readonly=True, default='liquidazione.xml')

    @api.multi
    def export(self):

        comunicazione_ids = self._context.get('active_ids')
        if not comunicazione_ids:
            raise exceptions.Warning(
                u'Attenzione! '
                u"Nessuna comunicazione selezionata"
            )
        if len(comunicazione_ids) > 1:
            raise exceptions.Warning(
                u'Attenzione! '
                u"E' possibile esportare una sola comunicazione alla volta"
            )

        for wizard in self:
            for comunicazione in self.env['comunicazione.liquidazione'].\
                    browse(comunicazione_ids):
                out = base64.encodestring(comunicazione.get_export_xml())
                wizard.file_export = out
            model_data_obj = self.env['ir.model.data']
            view_rec = model_data_obj.get_object_reference(
                'l10n_it_comunicazione_liquidazione_iva',
                'wizard_liquidazione_export_file_exit'
            )
            view_id = view_rec and view_rec[1] or False

            return {
                'view_type': 'form',
                'view_id': [view_id],
                'view_mode': 'form',
                'res_model': 'comunicazione.liquidazione.export.file',
                'res_id': wizard.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
