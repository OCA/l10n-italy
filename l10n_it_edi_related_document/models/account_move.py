from odoo import api, fields, models

from odoo.addons.l10n_it_edi.models.account_move import get_text


class AccountMoveRelatedDocumentType(models.Model):
    _name = "account.move.related_document"
    _description = "E-invoice Related Documents"

    type = fields.Selection(
        [
            ("order", "Order"),
            ("contract", "Contract"),
            ("agreement", "Agreement"),
            ("reception", "Reception"),
            ("invoice", "Related Invoice"),
        ],
        "Document",
        required=True,
    )
    name = fields.Char("Document ID", size=20, required=True)
    lineRef = fields.Integer("Line Ref.")
    invoice_id = fields.Many2one(
        "account.move",
        "Related Invoice",
        ondelete="cascade",
        index=True,
        readonly=True,
    )
    date = fields.Date()
    numitem = fields.Char("Item Num.", size=20)
    code = fields.Char("Order Agreement Code", size=100)
    cig = fields.Char("CIG Code", size=15)
    cup = fields.Char("CUP Code", size=15)
    invoice_line_id = fields.Many2one(
        "account.move.line",
        "Related Invoice Line",
        ondelete="cascade",
        index=True,
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        line_obj = self.env["account.move.line"]
        for vals in vals_list:
            if (
                vals.get("lineRef")
                and not vals.get("invoice_line_id")
                and vals.get("invoice_id")
            ):
                line = line_obj.search(
                    [
                        ("move_id", "=", vals["invoice_id"]),
                        ("sequence", "=", vals["lineRef"]),
                    ],
                    limit=1,
                )
                if line:
                    vals["invoice_line_id"] = line.id
        return super().create(vals_list)


class AccountMove(models.Model):
    _inherit = "account.move"

    related_document_ids = fields.One2many(
        "account.move.related_document", "invoice_id", copy=False
    )

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values=pdf_values)
        updated_values = self.remove_redundant_values(res)
        return updated_values

    def remove_redundant_values(self, values):
        redundant_list = [
            "cig",
            "cup",
            "origin_document_type",
            "origin_document_name",
            "origin_document_date",
        ]
        for key in redundant_list:
            values.pop(key, None)
        return values

    def _l10n_it_edi_import_invoice(self, invoice, data, is_new):
        res = super()._l10n_it_edi_import_invoice(invoice, data, is_new)
        tree = data["xml_tree"]
        rel_docs_dict = {
            "order": tree.xpath(".//DatiOrdineAcquisto"),
            "contract": tree.xpath(".//DatiContratto"),
            "agreement": tree.xpath(".//DatiConvenzione"),
            "reception": tree.xpath(".//DatiRicezione"),
            "invoice": tree.xpath(".//DatiFattureCollegate"),
        }
        self.create_related_document(invoice, rel_docs_dict)
        return res

    def create_related_document(self, invoice, rel_docs_dict):
        result = []
        invoice_line_model = self.env["account.move.line"]
        for key, rel_doc in rel_docs_dict.items():
            for element in rel_doc:
                invoice_lineid = False
                lineRef = get_text(element, "./RiferimentoNumeroLinea")
                if lineRef:
                    invoice_line = invoice_line_model.search(
                        [
                            ("move_id", "=", invoice.id),
                            ("sequence", "=", int(lineRef)),
                        ],
                        limit=1,
                    )
                    if invoice_line:
                        invoice_lineid = invoice_line.id
                entry = {
                    "type": key,
                    "lineRef": lineRef,
                    "name": get_text(element, "./IdDocumento"),
                    "date": get_text(element, "./Data"),
                    "numitem": get_text(element, "./NumItem"),
                    "code": get_text(element, "./CodiceCommessaConvenzione"),
                    "cup": get_text(element, "./CodiceCUP"),
                    "cig": get_text(element, "./CodiceCIG"),
                    "invoice_id": invoice.id,
                    "invoice_line_id": invoice_lineid,
                }
                entry = {k: v for k, v in entry.items() if v}
                result.append(entry)
        model = self.env["account.move.related_document"]
        model.create(result)
        return result
