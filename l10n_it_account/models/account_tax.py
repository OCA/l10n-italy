# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    cee_type = fields.Selection(
        [("sale", "Sale"), ("purchase", "Purchase")],
        string="Include in VAT register",
        help="Use in the case of tax with 'VAT integration'. This "
        "specifies the VAT register (sales / purchases) where the "
        "tax must be computed.",
    )
    parent_tax_ids = fields.Many2many(
        "account.tax",
        "account_tax_filiation_rel",
        "child_tax",
        "parent_tax",
        string="Parent Taxes",
    )

    def _get_tax_amount(self):
        self.ensure_one()
        res = 0.0
        if self.amount_type == "group":
            for child in self.children_tax_ids:
                res += child.amount
        else:
            res = self.amount
        return res

    def _get_tax_name(self):
        self.ensure_one()
        name = self.name
        if self.parent_tax_ids and len(self.parent_tax_ids) == 1:
            name = self.parent_tax_ids[0].name
        return name

    def _compute_totals_tax(self, data):
        """
        Args:
            data: date range, journals and registry_type
        Returns:
            A tuple: (tax_name, base, tax, deductible, undeductible)

        """
        self.ensure_one()
        context = {
            "from_date": data["from_date"],
            "to_date": data["to_date"],
        }
        registry_type = data.get("registry_type", "customer")
        if data.get("journal_ids"):
            context["vat_registry_journal_ids"] = data["journal_ids"]

        tax = self.env["account.tax"].with_context(context).browse(self.id)
        account_move_line_obj = self.env['account.move.line']
        tax_name = tax._get_tax_name()
        move_line_tax = account_move_line_obj.search([('date','>=', context.get('from_date')),
                                                               ('date','<=', context.get('to_date')),
                                                               ('tax_ids','in', tax.ids)])  
        move_line_tax_generated = account_move_line_obj.search([('date','>=', context.get('from_date')),
                                                                   ('date','<=', context.get('to_date')),
                                                                   ('tax_line_id','=', tax.id)])
        if registry_type == "supplier":
            debit_imponibile = -sum(move_line_tax.mapped('debit'))
            tax_amount = -sum(move_line_tax_generated.mapped('debit'))
        else:
            debit_imponibile = sum(move_line_tax.mapped('credit'))
            tax_amount = sum(move_line_tax_generated.mapped('credit'))                
        deductible = tax_amount
        undeductible = 0.0
        for child in tax.children_tax_ids:
            move_line_tax_generated = self.env['account.move.line'].search([('date','>=', context.get('from_date')),
                                                               ('date','<=', context.get('to_date')),
                                                               ('tax_line_id','=', child.id)])
            if child.cee_type:
                continue
            if registry_type == "supplier":
                tmp_amount = -sum(move_line_tax_generated.mapped('debit'))
            else:
                tmp_amount = sum(move_line_tax_generated.mapped('credit'))  
            #child.refund_repartition_line_ids.mapped("account_id")
            if any(child.invoice_repartition_line_ids.mapped('account_id')):
                deductible += tmp_amount
            else:
                undeductible += tmp_amount
        if not tax_amount:
            tax_amount = deductible + undeductible
        return (tax_name, debit_imponibile, tax_amount, deductible, undeductible)
