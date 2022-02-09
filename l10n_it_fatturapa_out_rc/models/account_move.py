from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def generate_self_invoice(self):
        res = super().generate_self_invoice()
        if self.rc_self_invoice_id:
            rc_type = self.fiscal_position_id.rc_type_id
            if rc_type.fiscal_document_type_id:
                self.rc_self_invoice_id.fiscal_document_type_id = (
                    rc_type.fiscal_document_type_id.id
                )
            if self.fatturapa_attachment_in_id:
                doc_id = self.fatturapa_attachment_in_id.name
            else:
                doc_id = self.ref if self.ref else self.name
            self.rc_self_invoice_id.related_documents = [
                (
                    0,
                    0,
                    {
                        "type": "invoice",
                        "name": doc_id,
                        "date": self.invoice_date,
                    },
                )
            ]
        return res

    def button_draft(self):
        super().button_draft()
        for inv in self:
            if not inv.env.context.get(
                "rc_set_to_draft"
            ) and inv.rc_purchase_invoice_id.state in ["draft", "cancel"]:
                raise UserError(
                    _(
                        "Vendor invoice that has generated this self invoice isn't "
                        "validated. "
                        "Validate vendor invoice before."
                    )
                )

    def preventive_checks(self):
        super().preventive_checks()
        invoices = self
        invoices_with_rc = invoices.filtered(lambda x: x.rc_purchase_invoice_id)
        # skip preventive checks when there are no invoices with rc
        if not invoices_with_rc:
            return
        invoices_without_rc = invoices - invoices_with_rc
        if invoices_without_rc:
            raise UserError(
                _(
                    "Selected invoices are both with and without reverse charge. You "
                    "should selected a smaller set of invoices"
                )
            )
        invoices_with_document_type_codes = invoices.filtered(
            lambda x: x.fiscal_document_type_id.code in ["TD17", "TD18", "TD19"]
        )
        invoices_without_document_type_codes = (
            invoices - invoices_with_document_type_codes
        )
        if invoices_with_document_type_codes and invoices_without_document_type_codes:
            raise UserError(
                _(
                    "Select invoices are of too many fiscal document types: "
                    "select invoices exclusively of type 'TD17', 'TD18', 'TD19' "
                    "or exclusively of other types."
                )
            )
        rc_suppliers = invoices_with_rc.mapped("rc_purchase_invoice_id.partner_id")
        if len(rc_suppliers) > 1:
            raise UserError(
                _(
                    "Selected reverse charge invoices have different suppliers. Please "
                    "select invoices with same supplier"
                )
            )
        # --- preventive checks related to set CedentePrestatore.DatiAnagrafici --- #
        partner = rc_suppliers and rc_suppliers[0] or self.env["res.partner"].browse()
        fiscal_document_type_codes = invoices_with_rc.mapped(
            "fiscal_document_type_id.code"
        )
        # Se vale IT , il sistema verifica che il TipoDocumento sia diverso da
        # TD17, TD18 e TD19; in caso contrario il file viene scartato
        vat = partner.vat and partner.vat[0:2]
        if vat:
            if vat == "IT" and any(
                [x in ["TD17", "TD18", "TD19"] for x in fiscal_document_type_codes]
            ):
                raise UserError(
                    _(
                        "A self-invoice cannot be issued with IT country code and "
                        "fiscal document type in 'TD17', 'TD18', 'TD19'."
                    )
                )
            if vat not in self.env["res.country"].search([]).mapped("code"):
                raise ValueError(
                    _(
                        "Country code does not exist or it is not mapped in countries: "
                        "%s" % vat
                    )
                )
        elif not partner.country_id.code or partner.country_id.code == "IT":
            raise UserError(
                _("Impossible to set IdFiscaleIVA for %s") % partner.display_name
            )
        # --- preventive checks related to set CedentePrestatore.Sede --- #
        if not partner.street:
            raise UserError(_("Partner %s, Street is not set.") % partner.display_name)
        if not partner.city:
            raise UserError(_("Partner %s, City is not set.") % partner.display_name)
        if not partner.country_id:
            raise UserError(_("Partner %s, Country is not set.") % partner.display_name)
        if not partner.zip:
            raise UserError(_("Partner %s, ZIP is not set.") % partner.display_name)
        return
