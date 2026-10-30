# Copyright 2026 nextev.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import _, api, fields, models


class OpenItemsReport(models.AbstractModel):
    _inherit = "report.account_financial_report.open_items"

    # ------------------------------------------------------------------
    # Calcolo dello scoperto
    # ------------------------------------------------------------------
    @api.model
    def _get_riba_uncovered_amounts(self, move_line_ids, date_at_object):
        """Ritorna {id riga fattura: importo scoperto RiBa}.

        Usa la stessa logica di account.move.open_amount: una riga è scoperta
        se ha il flag riba=True, tipo 'payment_term', e scadenza futura.
        Modificare la data di scadenza annulla immediatamente il valore.

        Le righe il cui incasso è stato formalmente registrato (stato RiBa
        'paid' o 'past_due') non sono considerate scoperte.
        """
        result = defaultdict(float)
        if not move_line_ids:
            return result
        today = fields.Date.today()
        _CLOSED_STATES = frozenset({"paid", "past_due", "cancel"})
        lines = self.env["account.move.line"].browse(list(move_line_ids))
        for line in lines.filtered(
            lambda ml: ml.riba
            and ml.display_type == "payment_term"
            and ml.date_maturity
            and ml.date_maturity > today
        ):
            slip_states = set(line.slip_line_ids.mapped("riba_line_id.state"))
            if slip_states and slip_states <= _CLOSED_STATES:
                continue
            result[line.id] = abs(line.balance)
        return result

    # ------------------------------------------------------------------
    # Righe aggiuntive (fatture chiuse dall'accettazione RiBa)
    # ------------------------------------------------------------------
    def _get_riba_closed_lines_domain(
        self,
        account_ids,
        partner_ids,
        date_at_object,
        only_posted_moves,
        company_id,
        date_from,
    ):
        domain = self._get_move_lines_domain_not_reconciled(
            company_id, account_ids, partner_ids, only_posted_moves, date_from
        )
        # Stesso dominio dello standard, ma sulle righe già riconciliate
        domain = [
            d for d in domain if not (isinstance(d, tuple) and d[0] == "reconciled")
        ]
        domain += [
            ("reconciled", "=", True),
            ("date", "<=", date_at_object),
            ("slip_line_ids.riba_line_id.state", "not in", ("draft", "cancel")),
        ]
        return domain

    def _riba_format_extra_line(self, move_line, grouped_by):
        """Prepara la riga con la stessa struttura delle righe standard."""
        partner = self.env["res.partner"]
        if move_line.get("partner_id"):
            partner = partner.browse(move_line["partner_id"][0])
        if grouped_by == "salesperson":
            group_id = partner.user_id.id or 0
            group_name = partner.user_id.name or _("Missing Salesperson")
        elif grouped_by:
            group_id = partner.id or 0
            group_name = partner.name or _("Missing Partner")
        else:
            group_id = 0
            group_name = ""
        if move_line["credit"]:
            original = move_line["credit"] * (-1)
        else:
            original = move_line["debit"]
        ref, name = move_line["ref"], move_line["name"]
        if ref == name:
            ref_label = ref or ""
        elif not ref:
            ref_label = name
        elif not name:
            ref_label = ref
        else:
            ref_label = ref + " - " + name
        move_line.update(
            {
                "date_maturity": move_line["date_maturity"]
                and move_line["date_maturity"].strftime("%d/%m/%Y"),
                "original": original,
                # Il saldo resta zero: la fattura è chiusa contabilmente
                "amount_residual": 0.0,
                "amount_residual_currency": 0.0,
                "partner_id": partner.id or 0,
                "partner_name": partner.name or "",
                "ref_label": ref_label,
                "journal_id": move_line["journal_id"][0],
                "entry_id": move_line["move_id"][0],
                "currency_id": move_line["currency_id"][0]
                if move_line["currency_id"]
                else False,
                "currency_name": move_line["currency_id"][1]
                if move_line["currency_id"]
                else False,
                "riba_closed": True,
            }
        )
        return group_id, group_name

    @api.model
    def _riba_cap_uncovered(self, move_line, amount):
        """Lo scoperto non può superare la parte della riga già chiusa alla
        data del report (originale - residuo): se a quella data la fattura
        risulta ancora aperta, l'importo è già nel saldo e non va duplicato.
        """
        closed = abs(move_line["debit"] - move_line["credit"]) - abs(
            move_line["amount_residual"]
        )
        return max(min(amount, closed), 0.0)

    def _get_data(
        self,
        account_ids,
        partner_ids,
        date_at_object,
        only_posted_moves,
        company_id,
        date_from,
        grouped_by,
    ):
        res = super()._get_data(
            account_ids,
            partner_ids,
            date_at_object,
            only_posted_moves,
            company_id,
            date_from,
            grouped_by,
        )
        if not self.env.context.get("show_riba_uncovered"):
            return res
        (
            move_lines,
            partners_data,
            journals_data,
            accounts_data,
            open_items_move_lines_data,
        ) = res

        existing_ids = {ml["id"] for ml in move_lines}
        extra_lines = self.env["account.move.line"].search_read(
            domain=self._get_riba_closed_lines_domain(
                account_ids,
                partner_ids,
                date_at_object,
                only_posted_moves,
                company_id,
                date_from,
            ),
            fields=self._get_ml_fields(),
        )
        extra_lines = [ml for ml in extra_lines if ml["id"] not in existing_ids]

        uncovered = self._get_riba_uncovered_amounts(
            existing_ids | {ml["id"] for ml in extra_lines}, date_at_object
        )
        for ml in move_lines:
            ml["riba_uncovered"] = self._riba_cap_uncovered(
                ml, uncovered.get(ml["id"], 0.0)
            )
            ml.setdefault("riba_closed", False)

        currency = self.env["res.company"].browse(company_id).currency_id
        new_journal = False
        for ml in extra_lines:
            amount = uncovered.get(ml["id"], 0.0)
            if currency.is_zero(amount):
                continue
            ml["riba_uncovered"] = amount
            group_id, group_name = self._riba_format_extra_line(ml, grouped_by)
            if group_id not in partners_data:
                partners_data[group_id] = {"id": group_id, "name": group_name}
            if ml["journal_id"] not in journals_data:
                new_journal = True
            acc_id = ml["account_id"][0]
            open_items_move_lines_data.setdefault(acc_id, {}).setdefault(
                group_id, []
            ).append(ml)
            move_lines.append(ml)

        if new_journal:
            journals_data = self._get_journals_data(
                list({ml["journal_id"] for ml in move_lines})
            )
        missing_accounts = set(open_items_move_lines_data) - set(accounts_data)
        if missing_accounts:
            accounts_data = self._get_accounts_data(
                list(open_items_move_lines_data.keys())
            )
        return (
            move_lines,
            partners_data,
            journals_data,
            accounts_data,
            open_items_move_lines_data,
        )

    @api.model
    def _calculate_amounts(self, open_items_move_lines_data):
        total_amount = super()._calculate_amounts(open_items_move_lines_data)
        for account_id, by_partner in open_items_move_lines_data.items():
            total_amount[account_id]["riba_uncovered"] = 0.0
            for partner_id, lines in by_partner.items():
                amount = sum(line.get("riba_uncovered", 0.0) for line in lines)
                total_amount[account_id][partner_id]["riba_uncovered"] = amount
                total_amount[account_id]["riba_uncovered"] += amount
        return total_amount

    def _get_report_values(self, docids, data):
        show = bool(data.get("show_riba_uncovered"))
        res = super(
            OpenItemsReport, self.with_context(show_riba_uncovered=show)
        )._get_report_values(docids, data)
        res["show_riba_uncovered"] = show
        return res
