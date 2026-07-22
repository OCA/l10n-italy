# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import frozendict


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_split_payment = fields.Boolean(compute="_compute_is_split_payment", store=True)

    @api.depends("account_id", "company_id.sp_account_id")
    def _compute_is_split_payment(self):
        for line in self:
            line.is_split_payment = False
            if line.account_id and line.account_id == line.company_id.sp_account_id:
                line.is_split_payment = True

    def _compute_all_tax(self):
        res = None
        for line in self:
            res = super(AccountMoveLine, line)._compute_all_tax()
            new_compute_all_tax = {}
            for tax_key, tax_vals in line.compute_all_tax.items():
                if (
                    tax_key.get("tax_repartition_line_id")
                    and tax_key.get("display_type")
                    and not tax_key.get("is_split_payment")
                ):
                    new_tax_key = dict(tax_key)
                    new_tax_key["is_split_payment"] = False
                    tax_key = frozendict(new_tax_key)
                new_compute_all_tax[tax_key] = tax_vals
            line.compute_all_tax = new_compute_all_tax
        return res

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        move_computed = []
        for line in lines:
            if (
                line.move_id not in move_computed
                and line.display_type == "tax"
                and line.move_id.split_payment
                and not line.is_split_payment
                and not any(ml.is_split_payment for ml in line.move_id.line_ids)
            ):
                write_off_line_vals = line.move_id._build_writeoff_line()
                with line.move_id._sync_dynamic_lines(
                    container={"records": line.move_id}
                ):
                    line.move_id.line_ids = [(0, 0, write_off_line_vals)]
                move_computed.append(line.move_id)
        return lines
