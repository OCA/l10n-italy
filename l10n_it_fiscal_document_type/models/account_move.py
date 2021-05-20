from odoo import api, fields, models

from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    is_inadvaced_invoice = fields.Boolean("Is a in advanced invoice ?", default=False)
    
    @api.depends("partner_id", "journal_id", "move_type", "fiscal_position_id")
    def _compute_set_document_fiscal_type(self, force_update=False):
        for self_id in self:
            if not force_update:
                if self_id.state != "draft" and self_id.fiscal_document_type_id:
                    continue
            self_id.fiscal_document_type_id = False
            dt = self_id._get_document_fiscal_type()
            if dt:
                self_id.fiscal_document_type_id = dt.id
    
    def _get_document_fiscal_type(self):
        if self.move_type in 'out_invoice':
            domain = [('out_invoice','=', True)]
            if self.is_inadvaced_invoice:
                domain.append(("is_inadvaced", "=", True)) 
        elif self.move_type in'out_refund':
            domain = [('out_refund','=', True)]
        elif self.move_type in'in_invoice':
            domain = [('in_invoice','=', True)]
        elif self.move_type in'in_refund':
            domain = [('in_refund','=', True)]

        if self.journal_id:
            jornalDomain = domain + [("journal_ids", "in", [self.journal_id.id])]
        doc_id = False
        if self.partner_id:
            if self.move_type in ("out_invoice"):
                doc_id = self.partner_id.out_fiscal_document_type.id or False
            elif self.move_type in ("in_invoice"):
                doc_id = self.partner_id.in_fiscal_document_type.id or False
        suitable_documentType = self.env["fiscal.document.type"].search(jornalDomain)
        if not suitable_documentType:
            suitable_documentType = self.env["fiscal.document.type"].search(domain)
        if doc_id and suitable_documentType:
            if doc_id.id in suitable_documentType.ids:
                return doc_id
            else:
                raise UserError("Unable to found document type for move_type %s jornal_ids %s" % (self.move_type, self.journal_id.id))
        for fiscal_document_type in suitable_documentType:
            return fiscal_document_type

    fiscal_document_type_id = fields.Many2one(
        "fiscal.document.type",
        string="Fiscal Document Type",
        compute="_compute_set_document_fiscal_type",
        store=True,
        readonly=False,
    )
