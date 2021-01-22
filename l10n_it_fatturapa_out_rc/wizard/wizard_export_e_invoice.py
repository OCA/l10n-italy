from odoo import models, _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    IdFiscaleType,
    AnagraficaType,
    IndirizzoType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def exportInvoiceXML(
        self, company, partner, invoice_ids, attach=False, context=None
    ):
        if context is None:
            context = {}
        invoices = self.env["account.invoice"].browse(invoice_ids)
        invoices_with_rc = False
        invoices_without_rc = False
        for invoice in invoices:
            if invoice.rc_purchase_invoice_id:
                invoices_with_rc = True
            else:
                invoices_without_rc = True
        if invoices_with_rc and invoices_without_rc:
            raise UserError(_(
                "Selected invoices are both with and without reverse charge. You "
                "should selected a smaller set of invoices"))
        rc_suppliers = invoices.mapped("rc_purchase_invoice_id.partner_id")
        if len(rc_suppliers) > 1:
            raise UserError(_(
                "Selected reverse charge invoices have different suppliers. Please "
                "select invoices with same supplier"))
        if rc_suppliers:
            context['rc_supplier'] = rc_suppliers[0]
        return super(WizardExportFatturapa, self).exportInvoiceXML(
            company, partner, invoice_ids, attach, context)

    def _setDatiAnagraficiCedente(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setDatiAnagraficiCedente(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            partner = self.env.context["rc_supplier"]
            CedentePrestatore.DatiAnagrafici.CodiceFiscale = None
            if partner.vat:
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
        return res
