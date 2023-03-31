from odoo import api, fields, models


class FiscalDocumentType(models.Model):
    _name = "fiscal.document.type"
    _description = "Fiscal document type"

    code = fields.Char(string="Code", size=5, required=True)
    name = fields.Char(string="Name", size=100, required=True)
    out_invoice = fields.Boolean(string="Customer Invoice")
    in_invoice = fields.Boolean(string="Vendor Bill")
    out_refund = fields.Boolean(string="Customer Credit Note")
    in_refund = fields.Boolean(string="Vendor Credit Note")
    priority = fields.Integer(string="Priority", default="3")

    journal_ids = fields.Many2many(
        "account.journal",
        "account_journal_fiscal_doc_type_rel",
        "fiscal_document_type_id",
        "journal_id",
        "Journals",
    )

    refund_fiscal_document_type_id = fields.Many2one(
        "fiscal.document.type", string="Fiscal document for refund"
    )

    _order = "code, priority asc"

    @api.model
    def create(self, vals):
        res = super(FiscalDocumentType, self).create(vals)
        res.journal_ids.check_doc_type_relation()
        return res

    def write(self, vals):
        res = super(FiscalDocumentType, self).write(vals)
        for doc in self:
            doc.journal_ids.check_doc_type_relation()
        return res

    def name_get(self):
        res = []
        for doc_type in self:
            res.append((doc_type.id, "[%s] %s" % (doc_type.code, doc_type.name)))
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if not args:
            args = []
        if name:
            records = self.search(
                ["|", ("name", operator, name), ("code", operator, name)] + args,
                limit=limit,
            )
        else:
            records = self.search(args, limit=limit)
        return records.name_get()
