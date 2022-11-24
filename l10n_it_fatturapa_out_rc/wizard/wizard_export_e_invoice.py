from odoo import models, _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    IdFiscaleType,
    AnagraficaType,
    IndirizzoType
)
from odoo.fields import first


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def group_invoices_by_partner(self):
        """
        Group Reverse charge self-invoices one by one.

        We are sending invoices to ourselves,
        and XMLs containing self-invoices are currently managed as
        if there was one self-invoice in each XML
        (see `fatturapa.attachment.in.is_self_invoice`
        and `fatturapa.attachment.in.linked_invoice_id_xml`)
        """
        invoice_ids = self.env.context.get('active_ids', False)
        invoices = self._get_rc_invoices(invoice_ids)
        invoices_with_rc, _other_invoices = self._split_rc_invoices(invoices)
        if invoices == invoices_with_rc:
            # These are self-invoices, they are all for ourselves
            partner = first(invoices_with_rc).partner_id
            invoices_by_partner = {
                partner: [
                    invoice_with_rc.ids
                    for invoice_with_rc in invoices_with_rc
                ],
            }
        else:
            invoices_by_partner = super().group_invoices_by_partner()
        return invoices_by_partner

    def _split_rc_invoices(self, invoices):
        invoices_with_rc = invoices.filtered('rc_purchase_invoice_id')
        invoices_without_rc = invoices - invoices_with_rc
        return invoices_with_rc, invoices_without_rc

    def _get_rc_invoices(self, invoice_ids):
        """
        Return the invoices having IDs `invoice_ids`,
        if they satisfy Reverse Charge constraints;
        otherwise raise an Exception.
        """
        invoices = self.env["account.invoice"].browse(invoice_ids)
        # All the invoices are either self-invoices or not
        invoices_with_rc, invoices_without_rc = self._split_rc_invoices(invoices)
        if invoices_with_rc and invoices_without_rc:
            raise UserError(_(
                "Selected invoices are both with and without reverse charge. You "
                "should selected a smaller set of invoices"))

        # All the invoices either have specific fiscal document types or not
        fiscal_document_codes = ['TD17', 'TD18', 'TD19']
        invoices_fiscal_document_type_codes = invoices.filtered(
            lambda x: x.fiscal_document_type_id.code in fiscal_document_codes
        )
        invoices_fiscal_document_type1_codes = invoices.filtered(
            lambda x: x.fiscal_document_type_id.code not in fiscal_document_codes
        )
        if invoices_fiscal_document_type_codes and invoices_fiscal_document_type1_codes:
            raise UserError(_(
                "Select invoices are of too many fiscal document types: "
                "select invoices exclusively of type 'TD17', 'TD18', 'TD19' "
                "or exclusively of other types."
            ))
        return invoices

    def _get_rc_suppliers(self, invoices):
        rc_suppliers = invoices._get_original_suppliers()
        if len(rc_suppliers) > 1:
            raise UserError(_(
                "Selected reverse charge invoices have different suppliers. Please "
                "select invoices with same supplier"))
        return rc_suppliers

    def exportInvoiceXML(
        self, company, partner, invoice_ids, attach=False, context=None
    ):
        if context is None:
            context = {}
        invoices = self._get_rc_invoices(invoice_ids)
        rc_suppliers = self._get_rc_suppliers(invoices)
        if rc_suppliers:
            context['rc_supplier'] = rc_suppliers[0]
            context['invoices_fiscal_document_type_codes'] = invoices.mapped(
                'fiscal_document_type_id.code')
        return super(WizardExportFatturapa, self).exportInvoiceXML(
            company, partner, invoice_ids, attach, context)

    def _setDatiAnagraficiCedente(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setDatiAnagraficiCedente(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            partner = self.env.context["rc_supplier"]
            CedentePrestatore.DatiAnagrafici.CodiceFiscale = None
            fiscal_document_type_codes = self.env.context.get(
                'invoices_fiscal_document_type_codes')
            # Se vale IT , il sistema verifica che il TipoDocumento sia diverso da
            # TD17, TD18 e TD19; in caso contrario il file viene scartato
            if partner.vat:
                if partner.vat[0:2] == 'IT' and any([x in ['TD17', 'TD18', 'TD19'] for
                                                     x in fiscal_document_type_codes]):
                    raise UserError(_(
                        "A self-invoice cannot be issued with IT country code and "
                        "fiscal document type in 'TD17', 'TD18', 'TD19'."
                    ))
                if partner.vat[0:2] not in self.env['res.country'].search([]).\
                        mapped('code'):
                    raise ValueError(_(
                        "Country code does not exist or it is not mapped in countries: "
                        "%s" % partner.vat[0:2]
                    ))
                CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                    IdPaese=partner.vat[0:2], IdCodice=partner.vat[2:])
            elif partner.country_id.code and partner.country_id.code != 'IT':
                CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                    IdPaese=partner.country_id.code, IdCodice='99999999999')
            else:
                raise UserError(
                    _("Impossible to set IdFiscaleIVA for %s") % partner.display_name)
            CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=partner.name)
        return res

    def _setSedeCedente(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setSedeCedente(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            partner = self.env.context["rc_supplier"]
            if not partner.street:
                raise UserError(
                    _('Partner %s, Street is not set.') % partner.display_name)
            if not partner.city:
                raise UserError(
                    _('Partner %s, City is not set.') % partner.display_name)
            if not partner.country_id:
                raise UserError(
                    _('Partner %s, Country is not set.') % partner.display_name)
            if partner.codice_destinatario == 'XXXXXXX':
                CedentePrestatore.Sede = (
                    IndirizzoType(
                        Indirizzo=encode_for_export(partner.street, 60),
                        CAP='00000',
                        Comune=encode_for_export(partner.city, 60),
                        Provincia='EE',
                        Nazione=partner.country_id.code))
            else:
                if not partner.zip:
                    raise UserError(
                        _('Partner %s, ZIP is not set.') % partner.display_name)
                CedentePrestatore.Sede = IndirizzoType(
                    Indirizzo=encode_for_export(partner.street, 60),
                    CAP=partner.zip,
                    Comune=encode_for_export(partner.city, 60),
                    Nazione=partner.country_id.code)
                if partner.state_id:
                    CedentePrestatore.Sede.Provincia = partner.state_id.code
        return res

    def _setStabileOrganizzazione(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setStabileOrganizzazione(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.StabileOrganizzazione = None
        return res

    def _setRea(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setRea(CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.IscrizioneREA = None
        return res

    def _setContatti(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setContatti(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.Contatti = None
        return res

    def _setPubAdministrationRef(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setPubAdministrationRef(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.RiferimentoAmministrazione = None
        return res

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        if (
            invoice.rc_purchase_invoice_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id.rc_type_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id.rc_type_id.
                fiscal_document_type_id
        ):
            body.DatiGenerali.DatiGeneraliDocumento.TipoDocumento = (
                invoice.rc_purchase_invoice_id.fiscal_position_id.rc_type_id.
                fiscal_document_type_id.code
            )
        if invoice.type in ['out_refund', 'in_refund'] \
                and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']:
            body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento = \
                - body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento
        return res

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision
    ):
        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision)
        if line.invoice_id.type in ['out_refund', 'in_refund'] and \
                line.invoice_id.fiscal_document_type_id.code not in ['TD04', 'TD08']:
            DettaglioLinea.PrezzoUnitario = - DettaglioLinea.PrezzoUnitario
            DettaglioLinea.PrezzoTotale = - DettaglioLinea.PrezzoTotale
        return DettaglioLinea

    def setDatiRiepilogo(self, invoice, body):
        super(WizardExportFatturapa, self).setDatiRiepilogo(invoice, body)
        for DatiRiepilogo in body.DatiBeniServizi.DatiRiepilogo:
            if invoice.type in ['out_refund', 'in_refund'] \
                    and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']:
                DatiRiepilogo.ImponibileImporto = - DatiRiepilogo.ImponibileImporto
                DatiRiepilogo.Imposta = - DatiRiepilogo.Imposta
        return True

    def setDatiPagamento(self, invoice, body):
        super(WizardExportFatturapa, self).setDatiPagamento(invoice, body)
        for DatiPagamento in body.DatiPagamento:
            if invoice.type in ['out_refund', 'in_refund'] \
                    and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']\
                    and DatiPagamento.ImportoPagamento:
                DatiPagamento.ImportoPagamento = - DatiPagamento.ImportoPagamento
        return True
