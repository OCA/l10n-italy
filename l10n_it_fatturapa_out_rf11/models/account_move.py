from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Move(models.Model):
    _inherit = "account.move"

    agent_74ter_id = fields.Many2one("res.partner", string="Agency")
    to_be_paid_by_agent_74ter = fields.Boolean("To be paid by agency")
    is_partner_74ter_agent = fields.Boolean(related="partner_id.is_74ter_agent")

    @api.onchange("partner_id")
    def onchange_74ter_partner_id(self):
        if not self.partner_id.is_74ter_agent and self.partner_id.agent_74ter_id:
            self.agent_74ter_id = self.partner_id.agent_74ter_id
            if self.partner_id.invoices_paid_by_agent:
                self.to_be_paid_by_agent_74ter = True
        if self.partner_id.is_74ter_agent:
            self.agent_74ter_id = False
            self.to_be_paid_by_agent_74ter = False

    @api.onchange("agent_74ter_id")
    def onchange_agent_74ter_id(self):
        if not self.agent_74ter_id:
            self.to_be_paid_by_agent_74ter = False

    def _post(self, soft=True):
        to_post = super()._post(soft)
        for invoice in self.filtered(lambda move: move.is_invoice(include_receipts=True)):
            if invoice.agent_74ter_id and invoice.to_be_paid_by_agent_74ter:
                if not invoice.company_id.payments_74ter_journal_id:
                    raise UserError(_("Please set \"Journal for agencies payments\" in accounting settings"))
                credit_amount = 0
                line_names = []
                write_off_vals = []
                to_reconcile = self.env["account.move.line"]
                for line in invoice.line_ids:
                    if line.partner_id and line.amount_residual:
                        to_reconcile |= line
                        credit_amount += line.amount_residual
                        line_names.append(line.name)
                        write_off_vals.append([0, 0, {
                            "debit": line.credit,
                            "credit": line.debit,
                            "account_id": line.account_id.id,
                            "partner_id": line.partner_id.id,
                            "name": line.name,
                        }])
                if credit_amount != 0 and write_off_vals:
                    write_off_vals.append([0, 0, {
                        "debit": credit_amount if credit_amount > 0 else 0,
                        "credit": credit_amount if credit_amount < 0 else 0,
                        "account_id": invoice.agent_74ter_id.property_account_receivable_id.id,
                        "partner_id": invoice.agent_74ter_id.id,
                        "name": ", ".join(line_names),
                    }])
                move_vals = {
                    "journal_id": invoice.company_id.payments_74ter_journal_id.id,
                    "line_ids": write_off_vals,
                    "move_type": "entry",
                    "date": invoice.invoice_date,
                    "ref": invoice.ref,
                }
                move = self.env["account.move"].create(move_vals)
                move._post()
                to_reconcile |= move.line_ids.filtered(lambda l: l.partner_id == invoice.partner_id)
                to_reconcile.reconcile()
        return to_post