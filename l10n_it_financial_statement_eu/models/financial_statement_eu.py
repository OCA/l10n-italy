# Copyright 2022 MKT srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import operator

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang

_logger = logging.getLogger(__name__)


class FinancialStatementEU(models.Model):
    _name = "financial.statement.eu"
    _description = "Financial statement EU line"
    _rec_names_search = ["complete_name"]
    zone_bal = fields.Selection(
        [
            ("PA", "Assets"),
            ("PP", "Liabilities"),
            ("EC", "Income statement"),
            ("--", "Ignore"),
        ],
        string="Zone",
        required=True,
    )
    code = fields.Char(size=8)
    name = fields.Char(
        string="Description",
    )
    long_desc = fields.Char(
        string="Complete Description",
    )
    sign_calculation = fields.Selection(
        selection=[
            ("-", "Subtract"),
            ("", "Add"),
        ],
        string="Sign (calc)",
    )
    sign_display = fields.Selection(
        selection=[
            ("+", "Positive"),
            ("-", "Negative"),
        ],
        string="Sign (view)",
    )
    sequence = fields.Integer(
        string="#",
        required=False,
    )
    tag_xbrl = fields.Char(
        string="Name XBRL",
    )
    parent_id = fields.Many2one(
        comodel_name="financial.statement.eu",
        string="Parent",
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name="financial.statement.eu",
        inverse_name="parent_id",
        string="Childs",
    )
    complete_name = fields.Char(
        compute="_compute_complete_name", store=True, recursive=True
    )

    def get_parent_path(self):
        self.ensure_one()
        if self.parent_id:
            line = self.parent_id.get_parent_path()
        else:
            line = ""
        return line + self.name + " / "

    @api.depends("code", "name", "parent_id", "parent_id.complete_name")
    def _compute_complete_name(self):
        for line in self:
            if line.parent_id:
                p = line.parent_id.get_parent_path()
            else:
                p = ""
            line.complete_name = f"[{line.code}] {p}{line.name}"

    def name_get(self):
        res = []
        for line in self:
            res.append((line.id, line.complete_name))
        return res

    @api.constrains("code", "zone_bal")
    def _check_code_zone(self):
        for line in self:
            if (line.zone_bal == "PA") and (not line.code.startswith("PA")):
                raise ValidationError(_("ASSETS codes must starting by PA"))
            elif (line.zone_bal == "PP") and (not line.code.startswith("PP")):
                raise ValidationError(_("LIABILITIES codes must starting by PP"))
            elif (line.zone_bal == "EC") and (not line.code.startswith("E")):
                raise ValidationError(_("INCOME STATEMENT codes must starting by E"))

    @api.model
    def financial_statement_eu_account_association(
        self,
        acc_code,
        debit_fse_id,
        credit_fse_id,
        force_update,
    ):
        acc_ids = self.env["account.account"].search([("code", "=ilike", acc_code)])
        for acc_id in acc_ids:
            if (
                (not acc_id.financial_statement_eu_debit_id)
                and (not acc_id.financial_statement_eu_credit_id)
            ) or force_update:
                if (acc_id.financial_statement_eu_debit_id.id != debit_fse_id) or (
                    acc_id.financial_statement_eu_credit_id.id != credit_fse_id
                ):
                    acc_id.write(
                        {
                            "financial_statement_eu_debit_id": debit_fse_id,
                            "financial_statement_eu_credit_id": credit_fse_id,
                        }
                    )

    @api.model
    def financial_statement_eu_account_assoc_code(
        self,
        acc_code,
        debit_financial_statement_eu_code,
        credit_financial_statement_eu_code,
    ):
        if debit_financial_statement_eu_code:
            debit_fse_id = self.search(
                [("code", "=", debit_financial_statement_eu_code)]
            )
        else:
            debit_fse_id = False
        if credit_financial_statement_eu_code:
            credit_fse_id = self.search(
                [("code", "=", credit_financial_statement_eu_code)]
            )
        else:
            credit_fse_id = False
        if debit_fse_id or credit_fse_id:
            self.financial_statement_eu_account_association(
                acc_code,
                debit_fse_id,
                credit_fse_id,
                False,
            )

    def cal_financial_statement_eu_line_amount(
        self, financial_statement_eu_lines, code
    ):
        total_amount = 0
        rounded_amount = 0
        financial_statement_eu_child_ids = self.env["financial.statement.eu"].search(
            [
                (
                    "parent_id",
                    "=",
                    financial_statement_eu_lines[code]["financial_statement_line"].id,
                )
            ]
        )
        for child in financial_statement_eu_child_ids:
            if child.child_ids:
                self.cal_financial_statement_eu_line_amount(
                    financial_statement_eu_lines, child.code
                )
            if child.sign_calculation == "-":
                rounded_amount -= financial_statement_eu_lines[child.code][
                    "rounded_amount"
                ]
                total_amount -= financial_statement_eu_lines[child.code]["total_amount"]
            else:
                rounded_amount += financial_statement_eu_lines[child.code][
                    "rounded_amount"
                ]
                total_amount += financial_statement_eu_lines[child.code]["total_amount"]
        financial_statement_eu_lines[code]["rounded_amount"] = tools.float_round(
            rounded_amount, 2
        )
        financial_statement_eu_lines[code]["total_amount"] = total_amount

    def add_calc_type_domain(self, domain, calc_type, financial_statement_eu_id):
        if calc_type == "d":
            domain.append(
                ("financial_statement_eu_debit_id", "=", financial_statement_eu_id)
            )
        elif calc_type == "c":
            domain.append(
                ("financial_statement_eu_credit_id", "=", financial_statement_eu_id)
            )
        elif calc_type == "non_assoc":
            domain.append(("financial_statement_eu_debit_id", "=", False))
            domain.append(("financial_statement_eu_credit_id", "=", False))

    def get_account_list_amount(
        self,
        company_id,
        currency_id,
        date_from,
        date_to,
        only_posted_move,
        hide_acc_amount_0,
        ignore_closing_move,
        calc_type,
        financial_statement_eu_id,
        sign_display,
        financial_statement_line_amount,
        account_list,
    ):
        currency_precision = currency_id.decimal_places
        domain = []
        domain.append(("company_id", "=", company_id))
        self.add_calc_type_domain(domain, calc_type, financial_statement_eu_id)
        acc_model = self.env["account.account"]
        account_ids = acc_model.read_group(
            domain,
            fields=[
                "id",
                "code",
                "name",
                "financial_statement_eu_debit_id",
                "financial_statement_eu_credit_id",
            ],
            groupby=[
                "id",
                "code",
                "name",
                "financial_statement_eu_debit_id",
                "financial_statement_eu_credit_id",
            ],
            orderby="code",
            lazy=False,
        )
        if account_ids:
            for item in account_ids:
                account_id = False
                for d in item.get("__domain"):
                    if type(d) is tuple and d[0] == "id":
                        account_id = d[2]
                if account_id:
                    acc_credit_id = item.get("financial_statement_eu_credit_id")
                    acc_debit_id = item.get("financial_statement_eu_debit_id")
                    domain = []
                    domain.append(("company_id", "=", company_id))
                    domain.append(("account_id", "=", account_id))
                    domain.append(("date", ">=", date_from))
                    domain.append(("date", "<=", date_to))
                    if only_posted_move:
                        domain.append(("move_id.state", "=", "posted"))
                    if ignore_closing_move:
                        domain.append(("move_id.closing_type", "!=", "closing"))
                        domain.append(("move_id.closing_type", "!=", "loss_profit"))
                    aml_model = self.env["account.move.line"]
                    amls = aml_model.read_group(
                        domain,
                        ["debit", "credit", "account_id"],
                        ["account_id"],
                        lazy=False,
                    )
                    if amls:
                        for line in amls:
                            acc_amount = tools.float_round(
                                line.get("debit") - line.get("credit"),
                                currency_precision,
                            )
                            if (
                                (calc_type == "non_assoc")
                                or (
                                    (calc_type == "d")  # debit
                                    and (
                                        (
                                            currency_id.compare_amounts(acc_amount, 0)
                                            >= 0
                                        )
                                        or (not acc_credit_id)
                                    )
                                )
                                or (
                                    (calc_type == "c")  # credit
                                    and (
                                        (
                                            currency_id.compare_amounts(acc_amount, 0)
                                            == -1
                                        )
                                        or (not acc_debit_id)
                                    )
                                )
                            ):
                                if sign_display == "-":
                                    acc_amount = -acc_amount
                                financial_statement_line_amount = (
                                    financial_statement_line_amount + acc_amount
                                )
                                if (not hide_acc_amount_0) or (acc_amount != 0):
                                    account_list.append(
                                        {
                                            "code": item.get("code"),
                                            "desc": item.get("name"),
                                            "amount": acc_amount,
                                        }
                                    )
                    elif not hide_acc_amount_0:
                        account_list.append(
                            {
                                "code": item.get("code"),
                                "desc": item.get("name"),
                                "amount": 0,
                            }
                        )
        return financial_statement_line_amount

    def round_bal_val(self, val, precision):
        if precision == "u":
            return tools.float_round(val, 0)
        elif precision == "d":
            return tools.float_round(val, 2)
        else:
            return val

    def cal_financial_statement_eu_data(self, form_data):
        financial_statement_eu_lines = {}
        company_id = form_data["company_id"][0]
        currency_id = self.env["res.currency"].browse(form_data["currency_id"][0])
        date_from = form_data["date_from"]
        date_to = form_data["date_to"]
        only_posted_move = form_data["only_posted_move"]
        hide_acc_amount_0 = form_data["hide_acc_amount_0"]
        ignore_closing_move = form_data["ignore_closing_move"]
        if ignore_closing_move:
            if not self.env["account.move"].fields_get(allfields=["closing_type"]):
                ignore_closing_move = False
        financial_statement_eu_ids = self.search([])  # env["financial.statement.eu"].
        for item in financial_statement_eu_ids:
            financial_statement_eu_amount = 0
            account_list = []
            if not item.child_ids:
                calcs = ["d", "c"]  # d=debit c=credit
                for calc_type in calcs:
                    financial_statement_eu_amount = self.get_account_list_amount(
                        company_id,
                        currency_id,
                        date_from,
                        date_to,
                        only_posted_move,
                        hide_acc_amount_0,
                        ignore_closing_move,
                        calc_type,
                        item.id,
                        item.sign_display,
                        financial_statement_eu_amount,
                        account_list,
                    )
            account_list.sort(key=operator.itemgetter("code"))

            financial_statement_eu_amount_rounded = self.round_bal_val(
                financial_statement_eu_amount, form_data["values_precision"]
            )
            financial_statement_eu_lines[item.code] = {
                "financial_statement_line": item,
                "rounded_amount": financial_statement_eu_amount_rounded,
                "total_amount": financial_statement_eu_amount,
                "account_list": account_list,
            }
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "E.A")
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "E.B")
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "E.C")
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "E.D")
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "E.F")
        financial_statement_eu_lines["E=B"]["rounded_amount"] = (
            financial_statement_eu_lines["E.A"]["rounded_amount"]
            - financial_statement_eu_lines["E.B"]["rounded_amount"]
        )
        financial_statement_eu_lines["E=B"]["total_amount"] = (
            financial_statement_eu_lines["E.A"]["total_amount"]
            - financial_statement_eu_lines["E.B"]["total_amount"]
        )
        financial_statement_eu_lines["E=E"]["rounded_amount"] = (
            financial_statement_eu_lines["E=B"]["rounded_amount"]
            + financial_statement_eu_lines["E.C"]["rounded_amount"]
            + financial_statement_eu_lines["E.D"]["rounded_amount"]
        )
        financial_statement_eu_lines["E=E"]["total_amount"] = (
            financial_statement_eu_lines["E=B"]["total_amount"]
            + financial_statement_eu_lines["E.C"]["total_amount"]
            + financial_statement_eu_lines["E.D"]["total_amount"]
        )
        financial_statement_eu_lines["E=F"]["rounded_amount"] = (
            financial_statement_eu_lines["E=E"]["rounded_amount"]
            - financial_statement_eu_lines["E.F"]["rounded_amount"]
        )
        financial_statement_eu_lines["E=F"]["total_amount"] = (
            financial_statement_eu_lines["E=E"]["total_amount"]
            - financial_statement_eu_lines["E.F"]["total_amount"]
        )
        delta_ef = (
            self.round_bal_val(
                financial_statement_eu_lines["E=F"]["total_amount"],
                form_data["values_precision"],
            )
            - financial_statement_eu_lines["E=F"]["rounded_amount"]
        )
        if delta_ef != 0:
            financial_statement_eu_lines["E=A512"]["rounded_amount"] = delta_ef
            financial_statement_eu_lines["E.A51"]["rounded_amount"] += delta_ef
            financial_statement_eu_lines["E.A5"]["rounded_amount"] += delta_ef
            financial_statement_eu_lines["E.A"]["rounded_amount"] += delta_ef
            financial_statement_eu_lines["E=B"]["rounded_amount"] += delta_ef
            financial_statement_eu_lines["E=E"]["rounded_amount"] += delta_ef
            financial_statement_eu_lines["E=F"]["rounded_amount"] += delta_ef

        financial_statement_eu_lines["PP=A9"][
            "rounded_amount"
        ] = financial_statement_eu_lines["E=F"]["rounded_amount"]
        financial_statement_eu_lines["PP=A9"][
            "total_amount"
        ] = financial_statement_eu_lines["E=F"]["total_amount"]
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "PA")
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "PP")
        financial_statement_eu_lines["PP=A7j2"]["total_amount"] = (
            financial_statement_eu_lines["PA"]["rounded_amount"]
            - financial_statement_eu_lines["PP"]["rounded_amount"]
        ) - (
            financial_statement_eu_lines["PA"]["total_amount"]
            - financial_statement_eu_lines["PP"]["total_amount"]
        )

        financial_statement_eu_lines["PP=A7j2"]["rounded_amount"] = self.round_bal_val(
            financial_statement_eu_lines["PP=A7j2"]["total_amount"],
            form_data["values_precision"],
        )
        self.cal_financial_statement_eu_line_amount(financial_statement_eu_lines, "PP")
        log_warnings = ""
        acc_ignore = ""
        financial_statement_eu_lines_report_data = []
        for line in financial_statement_eu_lines:
            if (
                financial_statement_eu_lines[line]["financial_statement_line"].zone_bal
                != "--"
            ):
                financial_statement_eu_lines_report_data.append(
                    {
                        "code": financial_statement_eu_lines[line][
                            "financial_statement_line"
                        ].code,
                        "desc": financial_statement_eu_lines[line][
                            "financial_statement_line"
                        ].long_desc,
                        "amount": financial_statement_eu_lines[line]["rounded_amount"],
                        "accounts": financial_statement_eu_lines[line]["account_list"],
                    }
                )
            else:
                for acc in financial_statement_eu_lines[line]["account_list"]:
                    if acc["amount"] != 0:
                        acc_ignore += (
                            "   "
                            + acc["code"]
                            + " "
                            + acc["desc"]
                            + ": "
                            + formatLang(
                                self.env, acc["amount"], currency_obj=currency_id
                            )
                            + "\n"
                        )
        if acc_ignore != "":
            log_warnings += (
                _("There are accounts to ignore but with non-zero amount:")
                + "\n"
                + acc_ignore
            )
        financial_statement_state = "OK"
        log_env = self.env["financial.statement.eu.log"]
        log_env.search(
            [("financial_statement_id", "=", form_data["id"])]
        ).unlink()  # clear log
        unlinked_account = []
        tot = 0
        self.get_account_list_amount(
            company_id,
            currency_id,
            date_from,
            date_to,
            only_posted_move,
            hide_acc_amount_0,
            ignore_closing_move,
            "non_assoc",
            False,
            "",
            tot,
            unlinked_account,
        )
        if (
            financial_statement_eu_lines["PA"]["rounded_amount"]
            != financial_statement_eu_lines["PP"]["rounded_amount"]
        ):
            financial_statement_state = "UNBALANCED"
            log_warnings = log_warnings + (
                _(
                    "Unbalanced financial statements: "
                    "%(tot_assets)s (Assets) - %(tot_liabilities)s (Liabilities)"
                    " = %(diff)s"
                )
                % {
                    "tot_assets": formatLang(
                        self.env,
                        financial_statement_eu_lines["PA"]["rounded_amount"],
                        currency_obj=currency_id,
                    ),
                    "tot_liabilities": formatLang(
                        self.env,
                        financial_statement_eu_lines["PP"]["rounded_amount"],
                        currency_obj=currency_id,
                    ),
                    "diff": formatLang(
                        self.env,
                        tools.float_round(
                            financial_statement_eu_lines["PA"]["rounded_amount"]
                            - financial_statement_eu_lines["PP"]["rounded_amount"],
                            2,
                        ),
                        currency_obj=currency_id,
                    ),
                }
            )
        if len(unlinked_account) > 0:
            financial_statement_state = "UNLINKED_ACCOUNTS"
            log_warnings += (
                "\n"
                + _("There are accounts not linked to any financial statement line:")
                + "\n"
            )

            for acc in unlinked_account:
                account_id = (
                    self.env["account.account"]
                    .search([("code", "=", acc.get("code"))])
                    .id
                )
                log_env.create(
                    {
                        "financial_statement_id": form_data["id"],
                        "account_id": account_id,
                        "amount": acc.get("amount"),
                    }
                )
        log_warnings = log_warnings.strip()
        if log_warnings == "":
            warning_lines = []
        else:
            warning_lines = log_warnings.split("\n")
        data = {
            "form_data": form_data,
            "financial_statement_eu_lines": financial_statement_eu_lines_report_data,
            "financial_statement_state": financial_statement_state,
            "warnings": warning_lines,
            "unlinked_account": unlinked_account,
        }
        return data


class AccountRefFinancialStatementEU(models.Model):
    _inherit = "account.account"
    financial_statement_eu_debit_id = fields.Many2one(
        "financial.statement.eu",
        string="Debit (Financial statement EU)",
        domain="[('child_ids','=',False),"
        "'|', ('code','=','PP=A9'), ('code','not like','%=%')"
        "]",
        help="Add this account in a Financial statement EU line amount DEBITS",
    )
    financial_statement_eu_credit_id = fields.Many2one(
        "financial.statement.eu",
        string="Credit (Financial statement EU)",
        domain="[('child_ids','=',False),"
        "'|', ('code','=','PP=A9'), ('code','not like', '%=%')"
        "]",
        help="Add this account in a Financial statement EU line amount CREDITS",
    )
