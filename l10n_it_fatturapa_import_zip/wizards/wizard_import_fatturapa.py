#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError

ATTACHMENT_OUT_MODEL_NAME = "fatturapa.attachment.out"


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _is_import_attachment_out(self):
        model = self._get_selected_model()
        return model == ATTACHMENT_OUT_MODEL_NAME

    def _check_attachment(self, attachment):
        if self._is_import_attachment_out():
            if attachment.out_invoice_ids:
                raise UserError(
                    _("File %s is linked to invoices yet.", attachment.name)
                )
            result = True
        else:
            result = super()._check_attachment(attachment)
        return result

    def _get_invoice_partner_id(self, fatt):
        if self._is_import_attachment_out():
            partner_id = self.getPartnerBase(
                fatt.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici
            )
        else:
            partner_id = super()._get_invoice_partner_id(fatt)
        return partner_id

    def _extract_supplier(self, attachment):
        if self._is_import_attachment_out():
            partner = self.env.company.partner_id
        else:
            partner = super()._extract_supplier(attachment)
        return partner

    def _get_received_date(self, attachment):
        if self._is_import_attachment_out():
            received_date = None
        else:
            received_date = super()._get_received_date(attachment)
        return received_date

    def _get_journal_domain(self, company):
        if self._is_import_attachment_out():
            domain = [
                ("type", "=", "sale"),
                ("company_id", "=", company.id),
            ]
        else:
            domain = super()._get_journal_domain(company)
        return domain

    def _get_missing_journal_exception(self, company):
        if self._is_import_attachment_out():
            exception = UserError(
                _(
                    "Define a sale journal for this company: "
                    "'%(company)s' (id: %(company_id)d).",
                    company=company.name,
                    company_id=company.id,
                )
            )
        else:
            exception = super()._get_missing_journal_exception(company)
        return exception

    def _prepare_invoice_values(self, fatt, fatturapa_attachment, FatturaBody, partner):
        invoice_values = super()._prepare_invoice_values(
            fatt,
            fatturapa_attachment,
            FatturaBody,
            partner,
        )
        if self._is_import_attachment_out():
            invoice_values["fatturapa_attachment_out_id"] = invoice_values.pop(
                "fatturapa_attachment_in_id"
            )
        return invoice_values

    def _get_invoice_type(self, fiscal_document_type):
        if self._is_import_attachment_out():
            if fiscal_document_type.code == "TD04":
                invoice_type = "out_refund"
            else:
                invoice_type = "out_invoice"
        else:
            invoice_type = super()._get_invoice_type(fiscal_document_type)
        return invoice_type

    def _get_account_tax_domain(self, amount):
        tax_domain = super()._get_account_tax_domain(amount)
        if self._is_import_attachment_out():
            return [
                ("type_tax_use", "=", "sale")
                if item == ("type_tax_use", "=", "purchase")
                else item
                for item in tax_domain
            ]
        else:
            return tax_domain

    def set_payments_data(self, FatturaBody, invoice, partner_id):
        if self._is_import_attachment_out():
            return super().set_payments_data(
                FatturaBody, invoice, self.env.company.partner_id.id
            )
        else:
            return super().set_payments_data(FatturaBody, invoice, partner_id)
