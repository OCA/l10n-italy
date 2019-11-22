# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera - Level Prime Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging

from odoo import models, _
from odoo.exceptions import UserError

from odoo.addons.l10n_it_fatturapa_out.wizard.wizard_export_fatturapa import (
    fatturapaBDS
)

from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    FatturaElettronica,
    FatturaElettronicaBodyType
)

_logger = logging.getLogger(__name__)

try:
    from pyxb.exceptions_ import SimpleFacetValueError, SimpleTypeValueError
except ImportError as err:
    _logger.debug(err)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def updateAttachment(self, attach, fatturapa):
        attach_str = fatturapa.toxml(
            encoding="UTF-8",
            bds=fatturapaBDS,
        )
        fatturapaBDS.reset()
        attach.write({
            'datas': base64.encodestring(attach_str),
        })

    def reSetProgressivoInvio(self, attach, fatturapa):
        # Xml file name uses the format VAT_XXXXX.xml and we are interested
        # to get XXXXX
        file_id = attach.name.split('_')[1].split('.')[0]
        try:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
                ProgressivoInvio = file_id
        except (SimpleFacetValueError, SimpleTypeValueError) as e:
            msg = _(
                'FatturaElettronicaHeader.DatiTrasmissione.'
                'ProgressivoInvio:\n%s'
            ) % unicode(e)
            raise UserError(msg)
        return file_id

    def exportFatturaPARegenerate(self):
        invoice_obj = self.env['account.invoice']
        attachments = self.env['fatturapa.attachment.out']
        # Browse active invoice
        active_id = invoice_obj.browse(self._context.get('active_id'))
        # Search all the invoices belonging the same xml file
        invoice_ids = invoice_obj.search(
            [('fatturapa_attachment_out_id', '=',
             active_id.fatturapa_attachment_out_id.id)])

        partner = active_id.partner_id
        if partner.is_pa:
            fatturapa = FatturaElettronica(versione='FPA12')
        else:
            fatturapa = FatturaElettronica(versione='FPR12')

        company = self.env.user.company_id
        context_partner = self.env.context.copy()
        context_partner.update({'lang': partner.lang})

        try:
            self.with_context(context_partner).setFatturaElettronicaHeader(
                company, partner, fatturapa)
            for invoice_id in invoice_obj.with_context(context_partner).browse(
                    invoice_ids.ids):

                if self.report_print_menu:
                    self.generate_attach_report(invoice_id)
                invoice_body = FatturaElettronicaBodyType()
                invoice_id.preventive_checks()
                self.with_context(
                    context_partner
                ).setFatturaElettronicaBody(
                    invoice_id, invoice_body)
                fatturapa.FatturaElettronicaBody.append(invoice_body)
                # TODO DatiVeicoli

            self.reSetProgressivoInvio(
                active_id.fatturapa_attachment_out_id, fatturapa)
        except (SimpleFacetValueError, SimpleTypeValueError) as e:
            raise UserError(unicode(e))

        self.updateAttachment(
            active_id.fatturapa_attachment_out_id, fatturapa)

        attachments += active_id.fatturapa_attachment_out_id

        action = {
            'view_type': 'form',
            'name': "Re-Export Electronic Invoice",
            'res_model': 'fatturapa.attachment.out',
            'type': 'ir.actions.act_window',
            }

        if len(attachments) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = attachments[0].id
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', attachments.ids)]

        return action
