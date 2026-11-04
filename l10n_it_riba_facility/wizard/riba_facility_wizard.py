# Copyright 2026 Nextev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
import io
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import xlsxwriter

USED_STATES = ("credited", "paid", "past_due")


class RibaFacilityWizard(models.TransientModel):
    _name = "riba.facility.wizard"
    _description = "RiBa Bank Receipts Facility Computation"
    _rec_name = "name"

    name = fields.Char(compute="_compute_name")

    def _compute_name(self):
        label = self.env._("RiBa Bank Receipts Facility")
        for rec in self:
            rec.name = label

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(related="company_id.currency_id")
    date_from = fields.Date(
        string="Reference Date",
        required=True,
        default=fields.Date.context_today,
        help="Starting point (usually today).",
    )
    date_to = fields.Date(
        string="Target Date",
        required=True,
        default=lambda self: fields.Date.context_today(self) + timedelta(days=30),
    )
    bank_ids = fields.Many2many(
        "res.partner.bank",
        string="Banks",
        domain="[('id', 'in', available_bank_ids)]",
        help="Leave empty for all banks with a SBF RiBa configuration.",
    )
    available_bank_ids = fields.Many2many(
        "res.partner.bank",
        relation="riba_facility_wizard_available_bank_rel",
        compute="_compute_available_bank_ids",
    )
    summary_ids = fields.One2many(
        "riba.facility.summary", "wizard_id", string="Summary per Bank"
    )
    detail_ids = fields.One2many(
        "riba.facility.detail", "wizard_id", string="RiBa Detail"
    )
    computed = fields.Boolean()
    anomaly_count = fields.Integer(compute="_compute_anomaly_count")

    @api.depends("company_id")
    def _compute_available_bank_ids(self):
        for wizard in self:
            wizard.available_bank_ids = (
                wizard._get_sbf_configs()
                .filtered(lambda c: c.riba_facility_amount > 0)
                .bank_id
            )

    @api.depends("detail_ids.is_anomaly")
    def _compute_anomaly_count(self):
        for wizard in self:
            wizard.anomaly_count = len(wizard.detail_ids.filtered("is_anomaly"))

    def _get_sbf_configs(self):
        self.ensure_one()
        return self.env["riba.configuration"].search(
            [("company_id", "=", self.company_id.id), ("type", "=", "sbf")]
        )

    def _get_banks(self):
        if self.bank_ids:
            return self.bank_ids
        return (
            self._get_sbf_configs()
            .filtered(lambda c: c.riba_facility_amount > 0)
            .bank_id
        )

    def _get_slip_lines(self, banks, states):
        domain = [
            ("company_id", "=", self.company_id.id),
            ("slip_id.config_id.type", "=", "sbf"),
            ("slip_id.config_id.bank_id", "in", banks.ids),
            ("state", "in", list(states)),
        ]
        if "paid" in states:
            # Exclude historical lines that can never affect the computation:
            # non-credited lines with due_date before date_from are always free.
            domain += [
                "|",
                ("state", "=", "credited"),
                ("due_date", ">=", self.date_from),
            ]
        return self.env["riba.slip.line"].search(domain)

    def _get_account_balance(self, accounts, date):
        if not accounts:
            return 0.0
        groups = self.env["account.move.line"]._read_group(
            [
                ("account_id", "in", accounts.ids),
                ("parent_state", "=", "posted"),
                ("date", "<=", date),
                ("company_id", "=", self.company_id.id),
            ],
            aggregates=["balance:sum"],
        )
        return groups[0][0] or 0.0 if groups else 0.0

    def _compute_facility(self):
        self.ensure_one()
        if self.date_to < self.date_from:
            raise UserError(
                self.env._(
                    "The target date must be equal to or later than the reference date."
                )
            )
        banks = self._get_banks()
        if not banks:
            raise UserError(
                self.env._(
                    "No RiBa subject to collection configuration found for "
                    "this company."
                )
            )
        self.summary_ids.unlink()
        self.detail_ids.unlink()

        today = self.date_from
        target = self.date_to
        totals = defaultdict(lambda: {"used_from": 0.0, "used_to": 0.0})
        detail_vals = []
        for line in self._get_slip_lines(banks, USED_STATES):
            bank = line.slip_id.config_id.bank_id
            used_from = line._riba_facility_is_used_at(today)
            used_to = line._riba_facility_is_used_at(target)
            release_date = line._riba_facility_release_date()
            # Overdue without closing or past due entry: not committed,
            # but flagged as anomaly.
            is_anomaly = line.state == "credited" and release_date <= today
            if not (used_from or used_to or is_anomaly):
                continue
            amount = line.amount
            if used_from:
                totals[bank]["used_from"] += amount
            if used_to:
                totals[bank]["used_to"] += amount
            releasing = used_from and not used_to
            detail_vals.append(
                {
                    "wizard_id": self.id,
                    "bank_id": bank.id,
                    "slip_line_id": line.id,
                    "slip_id": line.slip_id.id,
                    "partner_id": line.partner_id.id,
                    "invoice_number": line.invoice_number,
                    "due_date": line.due_date,
                    "release_date": release_date,
                    "amount": amount,
                    "line_state": line.state,
                    "released_by_target": releasing,
                    "is_anomaly": is_anomaly,
                }
            )

        to_credit = defaultdict(float)
        for line in self._get_slip_lines(banks, ("confirmed",)):
            to_credit[line.slip_id.config_id.bank_id] += line.amount

        configs = self._get_sbf_configs()
        summary_vals = []
        for bank in banks:
            data = totals[bank]
            bank_configs = configs.filtered(lambda c, b=bank: c.bank_id == b)
            accounts = bank_configs.mapped("credit_account_id")
            facility_amount = sum(bank_configs.mapped("riba_facility_amount"))
            summary_vals.append(
                {
                    "wizard_id": self.id,
                    "bank_id": bank.id,
                    "facility_amount": facility_amount,
                    "used_from": data["used_from"],
                    "used_to": data["used_to"],
                    "available_from": facility_amount - data["used_from"],
                    "available_to": facility_amount - data["used_to"],
                    "to_credit": to_credit[bank],
                    "account_balance": self._get_account_balance(accounts, today),
                }
            )
        self.env["riba.facility.summary"].create(summary_vals)
        self.env["riba.facility.detail"].create(detail_vals)
        self.computed = True

    def action_compute(self):
        self._compute_facility()
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
            "name": self.env._("RiBa Bank Receipts Facility"),
        }

    def action_open_details(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_riba_facility.action_riba_facility_detail"
        )
        action["domain"] = [("wizard_id", "=", self.id)]
        action["context"] = {
            "search_default_filter_releasing": 1,
            "search_default_group_bank": 1,
            "search_default_group_due_month": 1,
        }
        return action

    def action_open_anomalies(self):
        action = self.action_open_details()
        action["context"] = {"search_default_filter_anomaly": 1}
        return action

    # ------------------------------------------------------------------
    # Export Excel
    # ------------------------------------------------------------------
    def action_export_xlsx(self):
        self.ensure_one()
        if not self.computed:
            self._compute_facility()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        bold = workbook.add_format({"bold": True, "bg_color": "#E8E8E8"})
        money = workbook.add_format({"num_format": "#,##0.00"})
        money_bold = workbook.add_format({"num_format": "#,##0.00", "bold": True})
        date_fmt = workbook.add_format({"num_format": "dd/mm/yyyy"})

        ws = workbook.add_worksheet("Summary")
        ws.write(
            0, 0, "RiBa Bank Receipts Facility", workbook.add_format({"bold": True})
        )
        ws.write(1, 0, "Reference Date")
        ws.write_datetime(1, 1, fields.Datetime.to_datetime(self.date_from), date_fmt)
        ws.write(2, 0, "Target Date")
        ws.write_datetime(2, 1, fields.Datetime.to_datetime(self.date_to), date_fmt)
        headers = [
            "Bank",
            "Bank Receipts Facility",
            "Committed Today",
            "Committed at Target",
            "Available at Target",
            "Submitted to Credit",
            "RiBa Account Balance",
        ]
        row = 4
        for col, header in enumerate(headers):
            ws.write(row, col, header, bold)
        money_fields = [
            "facility_amount",
            "used_from",
            "used_to",
            "available_to",
            "to_credit",
            "account_balance",
        ]
        for summary in self.summary_ids:
            row += 1
            ws.write(row, 0, summary.bank_id.display_name)
            for col, fname in enumerate(money_fields, start=1):
                ws.write_number(row, col, summary[fname], money)
        row += 1
        ws.write(row, 0, "Total", bold)
        for col, fname in enumerate(money_fields, start=1):
            if fname != "account_balance":
                ws.write_number(
                    row, col, sum(self.summary_ids.mapped(fname)), money_bold
                )
        ws.set_column(0, 0, 40)
        ws.set_column(1, len(headers), 18)

        ws = workbook.add_worksheet("Detail")
        headers = [
            "Bank",
            "Slip",
            "Customer",
            "Invoices",
            "Due Date",
            "Release Date",
            "Release Week",
            "Amount",
            "State",
            "Released by Target",
            "Anomaly",
        ]
        for col, header in enumerate(headers):
            ws.write(0, col, header, bold)
        state_labels = dict(
            self.env["riba.facility.detail"]._fields["line_state"].selection
        )
        for row, det in enumerate(
            self.detail_ids.sorted(lambda d: (d.bank_id.id, d.release_date)), start=1
        ):
            ws.write(row, 0, det.bank_id.display_name)
            ws.write(row, 1, det.slip_id.name or "")
            ws.write(row, 2, det.partner_id.display_name or "")
            ws.write(row, 3, det.invoice_number or "")
            ws.write_datetime(
                row, 4, fields.Datetime.to_datetime(det.due_date), date_fmt
            )
            ws.write_datetime(
                row, 5, fields.Datetime.to_datetime(det.release_date), date_fmt
            )
            ws.write_datetime(
                row, 6, fields.Datetime.to_datetime(det.release_week), date_fmt
            )
            ws.write_number(row, 7, det.amount, money)
            ws.write(row, 8, state_labels.get(det.line_state, det.line_state or ""))
            ws.write(row, 9, "Yes" if det.released_by_target else "")
            ws.write(row, 10, "Overdue not Closed" if det.is_anomaly else "")
        ws.set_column(0, 3, 28)
        ws.set_column(4, 10, 16)
        ws.autofilter(0, 0, max(len(self.detail_ids), 1), len(headers) - 1)
        workbook.close()

        filename = f"riba_facility_{self.date_to.isoformat()}.xlsx"
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "datas": base64.b64encode(output.getvalue()),
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }


class RibaFacilitySummary(models.TransientModel):
    _name = "riba.facility.summary"
    _description = "RiBa Bank Receipts Facility: summary per bank"
    _order = "bank_id"

    wizard_id = fields.Many2one(
        "riba.facility.wizard", required=True, ondelete="cascade"
    )
    currency_id = fields.Many2one(related="wizard_id.currency_id")
    bank_id = fields.Many2one("res.partner.bank", string="Bank", readonly=True)
    facility_amount = fields.Monetary(string="Bank Receipts Facility", readonly=True)
    used_from = fields.Monetary(
        string="Committed Today",
        readonly=True,
        help="Credited RiBa slips not yet released at the reference date.",
    )
    available_from = fields.Monetary(string="Available Today", readonly=True)
    used_to = fields.Monetary(
        string="Committed at Target",
        readonly=True,
        help="Credited RiBa slips due after the target date.",
    )
    available_to = fields.Monetary(string="Available at Target", readonly=True)
    to_credit = fields.Monetary(
        string="Submitted to Credit",
        readonly=True,
        help="RiBa accepted by the bank but not yet credited: they will use the "
        "bank receipts facility when credited. Not included in the committed amount.",
    )
    account_balance = fields.Monetary(
        string="RiBa Account Balance",
        readonly=True,
        help="Accounting balance of the RiBa account (credit account of the SBF "
        "configurations for this bank) at the reference date. Used as a cross-check: "
        "if it differs from the committed amount, verify closings and past dues. "
        "If multiple banks share the same account, the balance is the combined total.",
    )


class RibaFacilityDetail(models.TransientModel):
    _name = "riba.facility.detail"
    _description = "RiBa Bank Receipts Facility: slip detail"
    _order = "bank_id, release_date, partner_id"

    wizard_id = fields.Many2one(
        "riba.facility.wizard", required=True, ondelete="cascade"
    )
    currency_id = fields.Many2one(related="wizard_id.currency_id")
    bank_id = fields.Many2one("res.partner.bank", string="Bank", readonly=True)
    slip_line_id = fields.Many2one("riba.slip.line", string="Slip Line", readonly=True)
    slip_id = fields.Many2one("riba.slip", string="Slip", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    invoice_number = fields.Char(string="Invoices", readonly=True)
    due_date = fields.Date(readonly=True)
    release_date = fields.Date(readonly=True)
    release_week = fields.Date(
        compute="_compute_release_week",
        store=True,
        help="Monday of the release week.",
    )
    amount = fields.Monetary(readonly=True)
    line_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Accepted"),
            ("credited", "Credited"),
            ("paid", "Paid"),
            ("past_due", "Past Due"),
            ("cancel", "Cancelled"),
        ],
        string="RiBa State",
        readonly=True,
    )
    released_by_target = fields.Boolean(string="Released by Target", readonly=True)
    is_anomaly = fields.Boolean(
        string="Overdue not Closed",
        readonly=True,
        help="RiBa still in credited state past the release date: "
        "closing or past due entry is missing.",
    )

    @api.depends("release_date")
    def _compute_release_week(self):
        for det in self:
            det.release_week = (
                det.release_date - timedelta(days=det.release_date.weekday())
                if det.release_date
                else False
            )
