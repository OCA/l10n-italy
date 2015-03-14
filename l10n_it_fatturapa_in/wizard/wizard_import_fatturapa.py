# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 AgileBG SAGL <http://www.agilebg.com>
#    Copyright (C) 2015 innoviu Srl <http://www.innoviu.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

from openerp.addons.l10n_it_fatturapa.bindings import fatturapa_v_1_1


class WizardImportFatturapa(orm.TransientModel):
    _name = "wizard.import.fatturapa"
    _description = "Import FatturaPA"

    def saveAttachment(self, cr, uid, context=None):
        if not context:
            context = {}

        return False

    def getPartnerId(self, cr, uid, cedPrest, fatPA, context=None):
        partner_model = self.pool['res.partner']
        cf = cedPrest.DatiAnagrafici.CodiceFiscale
        vat = "%s%s" % (
            cedPrest.DatiAnagrafici.IdFiscaleIVA.IdPaese,
            cedPrest.DatiAnagrafici.IdFiscaleIVA.IdCodice
        )
        partner_ids = partner_model.search(
            cr, uid,
            ['|',
             ('vat', '=', vat or 0),
             ('fiscalcode', '=', cf or 0),
             ],
            context=context)
        if len(partner_ids) > 1:
            raise orm.except_orm(
                _('Error !'),
                _("Two distinct partners with "
                  "Vat % and Fiscalcode % already present in db" %
                  (vat, cf))
                )
        if partner_ids:
            return partner_ids[0]
        else:
            vals = {
                'name': (
                    cedPrest.DatiAnagrafici.Anagrafica.Denominazione),
                'vat': vat,
                'fiscalcode': cf,
                'customer': False,
                'supplier': True,
                # TODO: needs verify
                'is_company': vat and True or False,
                'street': cedPrest.Sede.Indirizzo,
                'zip': cedPrest.Sede.CAP,
                'city': cedPrest.Sede.Comune,
                # FIXME add logic to get country id from name
                # 'country_id': xmlData.nazione,
            }
            if cedPrest.Contatti:
                vals['phone'] = cedPrest.Contatti.Telefono
                vals['email'] = cedPrest.Contatti.Email
                vals['fax'] = cedPrest.Contatti.Fax

            return partner_model.create(cr, uid, vals, context=context)

    def _prepareInvoiceLine(
        self, cr, uid, credit_account_id, line, context=None
    ):

        account_tax_model = self.pool['account.tax']
        account_tax_ids = account_tax_model.search(
            cr, uid,
            [
                ('type_tax_use', 'in', ('purchase', 'all')),
                ('amount', '=', float(line.AliquotaIVA) / 100),
            ], context=context)

        if not account_tax_ids:
            raise orm.except_orm(
                _('Error!'),
                _('Define a tax with percentage '
                  'equals to: "%s"'
                  % line.aliquotaIVA)
            )
        return {
            'name': line.Descrizione,
            'sequence': int(line.NumeroLinea),
            'account_id': credit_account_id,
            'price_unit': float(line.PrezzoUnitario),
            'quantity': float(line.Quantita),
            'invoice_line_tax_id': [(6, 0, [account_tax_ids[0]])],
        }

    def invoiceCreate(
        self, cr, uid, fatturapa_attachment, FatturaBody,
        partner_id, context=None
    ):
        if context is None:
            context = {}
        partner_model = self.pool['res.partner']
        journal_model = self.pool['account.journal']
        invoice_model = self.pool['account.invoice']
        currency_model = self.pool['res.currency']
        invoice_line_model = self.pool['account.invoice.line']

        company = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id
        partner = partner_model.browse(cr, uid, partner_id, context=context)
        pay_acc_id = partner.property_account_payable.id
        # FIXME: takes the first purchase journal without any check.
        journal_ids = journal_model.search(
            cr, uid,
            [
                ('type', '=', 'purchase'),
                ('company_id', '=', company.id)
            ],
            limit=1
            )
        if not journal_ids:
            raise orm.except_orm(
                _('Error!'),
                _(
                    'Define a purchase journal '
                    'for this company: "%s" (id:%d).'
                ) % (company.name, company.id))
        purchase_journal = journal_model.browse(
            cr, uid, journal_ids[0], context=context)
        # currency
        currency_id = currency_model.search(
            cr, uid,
            [
                (
                    'name', '=',
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            ],
            context=context)
        if not currency_id:
            raise orm.except_orm(
                _('Error!'),
                _(
                    'No currency found with code %s'
                    % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            )
        credit_account_id = purchase_journal.default_credit_account_id.id
        invoice_lines = []
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            invoice_line_data = self._prepareInvoiceLine(
                cr, uid, credit_account_id, line, context=context)
            invoice_line_id = invoice_line_model.create(
                cr, uid, invoice_line_data, context=context)
            invoice_lines.append(invoice_line_id)
        invoice_data = {
            'name': 'Fattura ' + partner.name,
            'date_invoice':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data,
            'supplier_invoice_number':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            # 'reference': xmlData.datiOrdineAcquisto,
            'account_id': pay_acc_id,
            'type': 'in_invoice',
            'partner_id': partner_id,
            'currency_id': currency_id[0],
            'journal_id': len(journal_ids) and journal_ids[0] or False,
            'invoice_line': [(6, 0, invoice_lines)],
            # 'origin': xmlData.datiOrdineAcquisto,
            'fiscal_position': False,
            'payment_term': False,
            'company_id': company.id,
            'fatturapa_attachment_in_id': fatturapa_attachment.id,
            'comment':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale[0],
        }
        invoice_id = invoice_model.create(
            cr, uid, invoice_data, context=context)
        # compute the invoice
        invoice_model.button_compute(
            cr, uid, [invoice_id], context=context,
            set_total=True)
        return invoice_id

    def importFatturaPA(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        fatturapa_attachment_obj = self.pool['fatturapa.attachment.in']
        fatturapa_attachment_ids = context.get('active_ids', False)
        new_invoices = []
        for fatturapa_attachment in fatturapa_attachment_obj.browse(
                cr, uid, fatturapa_attachment_ids, context=context):
            if fatturapa_attachment.in_invoice_ids:
                raise orm.except_orm(
                    _("Error"), _("File is linked to invoices yet"))
            #~ xmlData = XmlData(
                #~ fatturapa_attachment.datas.decode('base64')
            #~ )
            #~ xmlData.parseXml()
            fatt = fatturapa_v_1_1.CreateFromDocument(
                fatturapa_attachment.datas.decode('base64'))
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            partner_id = self.getPartnerId(
                cr, uid, cedentePrestatore, fatt, context=context)
            for fattura in fatt.FatturaElettronicaBody:
                #~ fattura = fatt.FatturaElettronicaBody[i]
                # TODO
                if (
                    fattura.DatiGenerali.DatiGeneraliDocumento.TipoDocumento in
                    ('TD04', 'TD05')
                ):
                    raise orm.except_orm(
                        _("Error"),
                        _("tipoDocumento %s not handled")
                        % fattura.tipoDocumento)
                invoice_id = self.invoiceCreate(
                    cr, uid, fatturapa_attachment, fattura,
                    partner_id, context=context)
                new_invoices.append(invoice_id)
        return {
            'view_type': 'form',
            'name': "PA Supplier Invoices",
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', new_invoices)],
            'context': context
            }
