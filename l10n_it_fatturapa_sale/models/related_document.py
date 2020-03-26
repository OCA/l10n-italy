#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FatturapaRelatedDocumentType(models.Model):
    _inherit = 'fatturapa.related_document_type'

    invoice_line_id = fields.Many2one(
        ondelete='set null',
    )
    invoice_id = fields.Many2one(
        ondelete='set null',
    )
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string="Sale order",
        index=True,
        readonly=True,
    )
    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Sale order line",
        index=True,
        readonly=True,
    )

    @api.multi
    def check_unlink(self):
        """
        Related documents only make sense if they are related (linked)
        to some other record.
        When this condition is no more satisfied,
        the document can be deleted.
        """
        to_delete = self.env[self._name].browse()
        check_fields = [
            'invoice_line_id',
            'invoice_id',
            'sale_order_id',
            'sale_order_line_id',
        ]
        for related_document in self:
            for check_field in check_fields:
                if related_document[check_field].exists():
                    break
            else:
                # `related_document` has to be deleted only
                # if none of the records in `check_fields` exists
                to_delete |= related_document
        return to_delete
