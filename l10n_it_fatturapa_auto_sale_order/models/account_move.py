from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        ret = super().create(vals_list)

        vl = []

        # consider only sale documents
        for move in ret.filtered(lambda m: m.is_sale_document()):
            # skip invoices that already have related documents of type "order",
            # assuming the user took care of the matter
            if move.related_documents.filtered(lambda rd: rd.type == "order"):
                continue

            for so in move.line_ids.sale_line_ids.order_id:
                v = {
                    "invoice_id": move.id,
                    "type": "order",
                    "name": f"{so.name} ({so.client_order_ref})"
                    if so.client_order_ref
                    else so.name,
                    "date": so.date_order,
                    "numitem": so.id,
                }
                vl.append(v)

        self.env["fatturapa.related_document_type"].create(vl)
        return ret
