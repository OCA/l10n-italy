from odoo import api, fields, models
from odoo.exceptions import UserError

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
        ret = super().create(vals_list)
        # after creating documents, check if one should is eligible
        # to become the standard_related_document_id
        for record in ret.filtered(
            lambda r: r.type in ("order", "contract", "agreement")
            and r.invoice_id
            and not r.invoice_id.standard_related_document_id
        ):
            invoice = record.invoice_id.with_context(
                l10n_it_edi_related_loop_avoid=True
            )
            invoice.standard_related_document_id = record
            invoice.l10n_it_origin_document_type = (
                "purchase_order" if record.type == "order" else record.type
            )
            invoice.l10n_it_origin_document_name = record.name
            invoice.l10n_it_origin_document_date = record.date
            invoice.l10n_it_cig = record.cig
            invoice.l10n_it_cup = record.cup

        return ret

    def _l10n_it_sync_related_document(self):
        for record in self:
            if record == record.invoice_id.standard_related_document_id:
                document_type = record.type
                if document_type == "order":
                    document_type = "purchase_order"
                elif document_type == "reception":
                    # unsupported type
                    record.invoice_id.standard_related_document_id = False
                    continue
                elif document_type == "invoice":
                    # unsupported type
                    record.invoice_id.standard_related_document_id = False
                    continue
                record.invoice_id.l10n_it_origin_document_type = document_type
                record.invoice_id.l10n_it_origin_document_name = record.name
                record.invoice_id.l10n_it_origin_document_date = record.date
                record.invoice_id.l10n_it_cig = record.cig
                record.invoice_id.l10n_it_cup = record.cup

    def write(self, vals):
        ret = super().write(vals)
        if self.env.context.get("l10n_it_edi_related_loop_avoid"):
            return ret
        if vals.keys() & {"type", "name", "date", "cig", "cup"}:
            self.with_context(
                l10n_it_edi_related_loop_avoid=True
            )._l10n_it_sync_related_document()
        return ret


class AccountMove(models.Model):
    _inherit = "account.move"

    related_document_ids = fields.One2many(
        "account.move.related_document", "invoice_id", copy=False
    )

    standard_related_document_id = fields.Many2one(
        comodel_name="account.move.related_document",
        string="Standard Related Document",
        help="Technical field to store the document corresponding to standard fields",
    )

    # override
    l10n_it_origin_document_type = fields.Selection(
        inverse="_inverse_original_related_document_fields"
    )
    l10n_it_origin_document_name = fields.Char(
        inverse="_inverse_original_related_document_fields"
    )
    l10n_it_origin_document_date = fields.Date(
        inverse="_inverse_original_related_document_fields"
    )
    l10n_it_cig = fields.Char(inverse="_inverse_original_related_document_fields")
    l10n_it_cup = fields.Char(inverse="_inverse_original_related_document_fields")

    def _inverse_original_related_document_fields(self):
        for record in self:
            if record.env.context.get("l10n_it_edi_related_loop_avoid"):
                continue
            if (
                not record.l10n_it_origin_document_type
                or not record.l10n_it_origin_document_name
            ):
                if record.standard_related_document_id:
                    # deleted reference
                    record.related_document_ids = [
                        fields.Command.unlink(record.standard_related_document_id.id)
                    ]
                    record.standard_related_document_id.unlink()
                    record.standard_related_document_id = False
                continue
            # type map
            # purchase_order -> order
            # contract -> contract
            # agreement -> agreement
            # ? -> reception
            # ? -> invoice
            document_type = record.l10n_it_origin_document_type
            if document_type == "purchase_order":
                document_type = "order"

            if (
                document_type
                not in dict(
                    self.env["account.move.related_document"]._fields["type"].selection
                ).keys()
            ):
                raise UserError(self.env._("Unknown document type %s", document_type))

            vals = {
                "type": document_type,
                "name": record.l10n_it_origin_document_name,
                "date": record.l10n_it_origin_document_date,
                "cig": record.l10n_it_cig,
                "cup": record.l10n_it_cup,
            }
            if not record.standard_related_document_id:
                record.standard_related_document_id = self.env[
                    "account.move.related_document"
                ].create(vals)
                record.related_document_ids = [
                    fields.Command.link(record.standard_related_document_id.id)
                ]
            else:
                record.standard_related_document_id.with_context(
                    l10n_it_edi_related_loop_avoid=True
                ).update(vals)

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
                name = get_text(element, "./IdDocumento")
                if not name:
                    continue
                entry = {
                    "type": key,
                    "lineRef": lineRef,
                    "name": name,
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
