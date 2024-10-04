# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time

from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang
from odoo.tools.translate import _


class ReportRegistroIva(models.AbstractModel):
    _name = "report.l10n_it_vat_registries.report_registro_iva"
    _description = "Report VAT registry"

    @api.model
    def _get_report_values(self, docids, data=None):
        # docids required by caller but not used

        date_format = data["form"]["date_format"]

        docargs = {
            "doc_ids": data["ids"],
            "doc_model": self.env["account.move"],
            "data": data["form"],
            "docs": self.env["account.move"].browse(data["ids"]),
            "get_move": self._get_move,
            "tax_lines": self._get_tax_lines,
            "format_date": self._format_date,
            "from_date": self._format_date(data["form"]["from_date"], date_format),
            "to_date": self._format_date(data["form"]["to_date"], date_format),
            "registry_type": data["form"]["registry_type"],
            "invoice_total": self._get_move_total,
            "tax_registry_name": data["form"]["tax_registry_name"],
            "env": self.env,
            "formatLang": formatLang,
            "compute_totals_tax": self._compute_totals_tax,
            "l10n_it_count_fiscal_page_base": data["form"]["fiscal_page_base"],
            "only_totals": data["form"]["only_totals"],
            "entry_order": data["form"].get("entry_order"),
            "show_full_contact_addess": data["form"]["show_full_contact_addess"],
            "date_format": date_format,
            "year_footer": data["form"]["year_footer"],
        }
        return docargs

    def _get_move(self, move_ids):
        move_list = self.env["account.move"].browse(move_ids)
        return move_list

    def _format_date(self, my_date, date_format):
        # supporting both cases, as data['form']['from_date'] is string
        if isinstance(my_date, str):
            formatted_date = time.strftime(
                date_format, time.strptime(my_date, "%Y-%m-%d")
            )
        else:
            formatted_date = my_date.strftime(date_format)
        return formatted_date or ""

    def _get_move_line(self, move, data):
        return [move_line for move_line in move.line_ids]

    def _tax_amounts_by_tax_id(self, move, move_lines, registry_type):
        res = {}

        for move_line in move_lines:
            if not (move_line.tax_line_id or move_line.tax_ids):
                continue

            if move_line.tax_ids and len(move_line.tax_ids) != 1:
                raise UserError(
                    _("Move line %s has too many base taxes") % move_line.name
                )

            if move_line.tax_ids:
                tax = move_line.tax_ids[0]
                is_base = True
            else:
                tax = move_line.tax_line_id
                is_base = False

            if tax.parent_tax_ids and len(tax.parent_tax_ids) == 1:
                # we group by main tax
                tax = tax.parent_tax_ids[0]

            if tax.exclude_from_registries:
                continue

            if not res.get(tax.id):
                res[tax.id] = {
                    "name": tax.name,
                    "base": 0,
                    "tax": 0,
                }
            tax_amount = move_line.debit - move_line.credit

            if (
                "receivable" in move.financial_type
                or "payable_refund" == move.financial_type
            ):
                # otherwise refund would be positive and invoices
                # negative.
                # We also check payable_refund as it normaly is < 0, but
                # it can be > 0 in case of reverse charge with VAT integration
                tax_amount = -tax_amount

            if is_base:
                # recupero il valore dell'imponibile
                res[tax.id]["base"] += tax_amount
            else:
                # recupero il valore dell'imposta
                res[tax.id]["tax"] += tax_amount

        return res

    def _get_tax_lines(self, move, data):

        """

        Args:
            move: the account.move representing the invoice

        Returns:
            A tuple of lists: (INVOICE_TAXES, TAXES_USED)
            where INVOICE_TAXES is a list of dict
            and TAXES_USED a recordset of account.tax

        """
        inv_taxes = []
        used_taxes = self.env["account.tax"]

        # index è usato per non ripetere la stampa dei dati fattura quando ci
        # sono più codici IVA
        index = 0
        if "refund" in move.move_type:
            invoice_type = "NC"
        else:
            invoice_type = "FA"

        move_lines = self._get_move_line(move, data)

        amounts_by_tax_id = self._tax_amounts_by_tax_id(
            move, move_lines, data["registry_type"]
        )

        for tax_id in amounts_by_tax_id:
            tax = self.env["account.tax"].browse(tax_id)
            tax_item = {
                "tax_code_name": tax._get_tax_name(),
                "base": amounts_by_tax_id[tax_id]["base"],
                "tax": amounts_by_tax_id[tax_id]["tax"],
                "index": index,
                "invoice_type": invoice_type,
                "invoice_date": (move.invoice_date or move.date or ""),
                "reference": (move.ref or move.name or ""),
                # These 4 items are added to make the dictionary more usable
                # in further customizations, allowing inheriting modules to
                # retrieve the records that have been used to create the
                # dictionary itself (instead of receiving a raw-data-only dict)
                "tax_rec": tax,
                "move_rec": move,
                "move_line_rec": self.env["account.move.line"].browse(
                    [move_line.id for move_line in move_lines]
                ),
                "invoice_rec": move,
            }
            inv_taxes.append(tax_item)
            index += 1
            used_taxes |= tax

        return inv_taxes, used_taxes

    def _get_move_total(self, move):

        total = 0.0
        receivable_payable_found = False
        for move_line in move.line_ids:
            if move_line.account_id.internal_type == "receivable":
                total += move_line.debit or (-move_line.credit)
                receivable_payable_found = True
            elif move_line.account_id.internal_type == "payable":
                total += (-move_line.debit) or move_line.credit
                receivable_payable_found = True
        if receivable_payable_found:
            total = abs(total)
        else:
            total = abs(move.amount_total)
        if "refund" in move.move_type:
            total = -total
        return total

    def _compute_totals_tax(self, tax, data):
        """
        Returns:
            A tuple: (tax_name, base, tax, deductible, undeductible)

        """
        return tax._compute_totals_tax(data)
