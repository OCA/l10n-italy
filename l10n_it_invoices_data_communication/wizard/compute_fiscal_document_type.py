from odoo import models


class ComunicazioneDatiIvaRicalcoloTipoDocumentoFiscale(models.TransientModel):
    _name = "comunicazione.dati.iva.ricalcolo.tipo.document.fiscale"
    _description = "Recompute invoices document type"

    def compute(self):
        comunicazione_ids = self._context.get("active_ids")
        for _wizard in self:
            for comunicazione in self.env["comunicazione.dati.iva"].browse(
                comunicazione_ids
            ):
                domain = [("comunicazione_dati_iva_escludi", "=", True)]
                no_journal_ids = self.env["account.journal"].search(domain).ids
                domain = [
                    ("state", "=", "posted"),
                    ("comunicazione_dati_iva_escludi", "!=", True),
                    ("journal_id", "not in", no_journal_ids),
                    ("company_id", ">=", comunicazione.company_id.id),
                    ("invoice_date", ">=", comunicazione.date_start),
                    ("invoice_date", "<=", comunicazione.date_end),
                ]
                fatture = self.env["account.move"].search(domain)
                for fattura in fatture:
                    fattura.fiscal_document_type_id = (
                        fattura._get_document_fiscal_type(
                            move_type=fattura.move_type,
                            partner=fattura.partner_id,
                            fiscal_position=fattura.fiscal_position_id,
                            journal=fattura.journal_id,
                        )[0]
                        or False
                    )
            return {}
