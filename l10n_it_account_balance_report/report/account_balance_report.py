# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.safe_eval import safe_eval


def get_xmlid(id_str):
    id_str = id_str.replace(".", "")
    return "l10n_it_account_balance_report.{}".format(id_str)


class ReportAccountBalanceReport(models.TransientModel):
    _name = "account_balance_report"
    _description = "Account balance report"
    _inherit = "report.account_financial_report.abstract_report"

    GROUP_TYPE = 'group_type'
    ACC_TYPE = 'account_type'

    account_balance_report_type = fields.Selection(
        [("profit_loss", "Profit & Loss"), ("balance_sheet", "Balance Sheet")],
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company.id,
        required=False,
        string="Company",
    )

    date_from = fields.Date()
    date_to = fields.Date()

    foreign_currency = fields.Boolean(
        string="Show foreign currency",
        help="Display foreign currency for move lines, unless "
        "account currency is not setup through chart of accounts "
        "will display initial and final balance in that currency.",
    )

    hide_account_at_0 = fields.Boolean(
        string="Hide accounts at 0",
        default=True,
        help="When this option is enabled, the trial balance will "
        "not display accounts that have initial balance = "
        "debit = credit = end balance = 0",
    )

    left_col_name = fields.Char()
    right_col_name = fields.Char()
    only_posted_moves = fields.Boolean(
        string="Display only posted moves"
    )
    section_credit_ids = fields.One2many(
        "account_balance_report_account", "report_credit_id"
    )
    section_debit_ids = fields.One2many(
        "account_balance_report_account", "report_debit_id"
    )

    show_hierarchy = fields.Boolean(
        string="Show hierarchy",
        help="Use when your account groups are hierarchical",
    )
    limit_hierarchy_level = fields.Boolean("Limit hierarchy levels")
    show_hierarchy_level = fields.Integer("Hierarchy Levels to display", default=1)
    hide_parent_hierarchy_level = fields.Boolean(
        "Do not display parent levels", default=False
    )

    show_partner_details = fields.Boolean()

    target_move = fields.Selection(
        [("posted", "All Posted Entries"), ("all", "All Entries")],
        string="Target Moves",
    )

    title = fields.Char()
    total_balance = fields.Float(digits=(16, 2))
    total_credit = fields.Float(digits=(16, 2))
    total_debit = fields.Float(digits=(16, 2))

    trial_balance_wiz_id = fields.Many2one(
        comodel_name="trial.balance.report.wizard"
    )

    def print_report(self, report_type=None):
        """

        :param report_type: string that represents the report type
        """
        self.ensure_one()
        tb_vals = self.trial_balance_wiz_id._prepare_report_trial_balance()
        trial_obj = self.env["report.account_financial_report.trial_balance"]
        tb_data = trial_obj._get_report_values(None, tb_vals)
        data = self.compute_data_for_report(tb_data)

        report_name = self._get_report_name(report_type)
        return (
            self.env["ir.actions.report"]
            .search(
                [
                    ("report_name", "=", report_name),
                    ("report_type", "=", report_type)
                ],
                limit=1,
            )
            .report_action(self, data=data)
        )

    @api.model
    def get_html(self, given_context=None):
        """Method needed from JavaScript widget to render HTML view"""
        context = dict(self.env.context)
        context.update(given_context or {})
        report = self or self.browse(context.get("active_id"))
        xml_id = get_xmlid("template_account_balance_report")

        result = {}
        if report:
            context["o"] = report
            result["html"] = self.env.ref(xml_id).render(context)
        return result

    def _get_report_name(self, report_type=None):
        if report_type == "xlsx":
            report_name = "l10n_it_a_b_r.account_balance_report_xlsx"
        elif report_type in ("qweb-pdf", "qweb-html"):
            report_name = get_xmlid("account_balance_report_qweb")
        else:
            raise ValidationError(
                _("No report type has been declared for current print.")
            )
        return report_name

    def do_print(self, report_type):
        self.ensure_one()
        if report_type == "qweb-pdf":
            xml_id = get_xmlid("report_account_balance_report_pdf")
        else:
            xml_id = get_xmlid("report_account_balance_report_xlsx")
        report = self.env.ref(xml_id)
        return report.report_action(self)

    def view_report(self):
        """Launches view for HTML report"""
        self.ensure_one()
        [act] = self.env.ref(get_xmlid("action_account_balance_report")).read()
        ctx = act.get("context", {})
        ctx = safe_eval(ctx)
        # Call update twice to force 'active_%s' values to be overridden
        ctx.update(dict(self._context))
        ctx.update(active_id=self.id, active_ids=self.ids)
        act["context"] = ctx
        return act

    def compute_data_for_report(self, tb_data):
        """
        Sets data for report.
        Defines which lines go on the left or right section, which names
        sections should have, the report title, amounts and balances
        """
        self.ensure_one()
        rep_type = self.account_balance_report_type

        # Trial balance already has every data we may need
        section_credit_vals = []
        section_debit_vals = []
        total_credit = 0
        total_debit = 0
        cols = self.get_column_data().get(rep_type)
        if not cols:
            raise ValidationError(
                _("Unknown report type; cannot parse it into a table.")
            )
        l_sec, l_name = cols["left"]["section"], cols["left"]["name"]
        r_sec, r_name = cols["right"]["section"], cols["right"]["name"]
        valid_sections = [l_sec, r_sec]

        curr = self.company_id.currency_id or self.company_id._get_euro()
        digits = curr.decimal_places

        if not digits:
            digits = self.env["decimal.precision"].precision_get("Account")

        if not self.show_partner_details:
            lines = tb_data['trial_balance']
        else:
            lines = tb_data['accounts_data'].values()

        for ln_data in lines:
            section = self.get_report_section(
                valid_sections,
                ln_data
            )

            if not (section and section in valid_sections):
                continue

            line_type = ln_data.get('type')
            if not self.show_partner_details:
                # Group line
                if line_type == self.GROUP_TYPE:
                    line_data = self._get_group_line_data(ln_data, digits)

                # Account line
                elif line_type == self.ACC_TYPE:
                    line_data = self._get_account_line_data(
                        ln_data,
                        digits
                    )
            else:
                line_data = self._get_account_line_data(
                    ln_data,
                    digits,
                    tb_data.get('partners_data', []),
                    tb_data.get('total_amount'),
                )

            balance_section_vals = self.get_section_balance_vals(
                line_data
            )

            total_debit, total_credit = self._insert_section_values(
                section,
                l_sec,
                r_sec,
                section_credit_vals,
                section_debit_vals,
                total_debit,
                total_credit,
                balance_section_vals,
                line_data,
                digits
            )

        if self.show_partner_details and self.show_hierarchy:
            credit_account_data = self._get_filtered_account(
                tb_data.get('accounts_data'),
                section_credit_vals
            )
            credit_group_data = self._get_group_data(
                credit_account_data,
                tb_data.get('total_amount')
            )
            self._compute_group_hierarchy(
                credit_group_data
            )
            self._add_group_to_section_vals(
                section_credit_vals,
                credit_group_data
            )
            debit_account_data = self._get_filtered_account(
                tb_data.get('accounts_data'),
                section_debit_vals
            )
            debit_group_data = self._get_group_data(
                debit_account_data,
                tb_data.get('total_amount')
            )
            self._compute_group_hierarchy(
                debit_group_data
            )
            self._add_group_to_section_vals(
                section_debit_vals,
                debit_group_data
            )

        total_balance = self.get_total_balance(
            total_debit,
            total_credit,
            digits
        )

        self.write(
            {
                "left_col_name": l_name,
                "right_col_name": r_name,
                "section_credit_ids": section_credit_vals,
                "section_debit_ids": section_debit_vals,
                "title": cols["title"],
                "total_balance": total_balance,
                "total_credit": total_credit,
                "total_debit": total_debit,
            }
        )

    def get_column_data(self):
        """
        This method is meant to be overridden if necessary.
        :returns: report data grouped by report type
        """
        return {
            "balance_sheet": {
                "left": {
                    "section": "assets",
                    "name": _("ASSETS"),
                },
                "right": {
                    "section": "liabilities",
                    "name": _("LIABILITIES"),
                },
                "title": _("BALANCE SHEET"),
            },
            "profit_loss": {
                "left": {
                    "section": "expenses",
                    "name": _("COSTS"),
                },
                "right": {
                    "section": "incomes",
                    "name": _("REVENUES"),
                },
                "title": _("PROFIT & LOSS"),
            },
        }

    def get_report_section(self, valid_sections, line):
        """Get section name where to insert account_balance_report_account
        line

        :param valid_sections: ``tuple(str)`` Allowed account type, to insert
            in correct section
        :param line: ``dict`` The line data, obtained from trial_balance

        :return: ``str`` The section name, where to insert this line
        """
        section = ""
        account = self.env['account.account']

        if line.get('type') == self.GROUP_TYPE:
            account = self._get_group_account(valid_sections, line)
        elif line.get('type') == self.ACC_TYPE or self.show_partner_details:
            account = self.env['account.account'].browse(
                line.get('id')
            ).exists()

        if account:
            section = account.account_balance_report_section
        return section

    def _get_group_account(self, valid_sections, line):
        """Get balance section from a group line

        if the examined line type is `group_type`, get the account.group
        record, and check if it had accounts; if no account are present, try
        to get accounts from line data; if at this stage no account are
        present, try to traverse backward the group tree to root node until
        find one with accounts

        :param valid_sections: ``tuple(str)`` Allowed account type, to
            insert in right section
        :param line: ``dict`` The line data, obtained from trial_balance

        :return: ``account.account`` The account to be used to compute
            section name
        """
        group = self.env['account.group'].browse(
            line.get('id')
        ).exists()
        if group and group.account_ids:
            accounts = group.account_ids
        elif group and not group.account_ids and group.parent_id:
            while group and group.parent_id and not group.account_ids:
                group = group.parent_id
            accounts = group.account_ids
        else:
            accounts = self.env['account.account'].browse(
                line.get('account_ids')
            ).exists()

        return accounts.filtered(
            lambda acc: acc.account_balance_report_section in valid_sections
        )[:1]

    def _get_group_line_data(self, line, digits):
        """Use data of group_type line to prepare the values to be inserted
        in `account_balance_report_account`

        :param line: ``dict`` The line data
        :param digits: ``int`` The rounding digits, used in float calc

        :return: ``dict`` The dictionary with data to be set in the
            section report
        """
        currency_data = self._get_foreign_currency_data(line, digits)
        group_id = line.get("id")
        r_data = {
            **line,
            **currency_data,
            "group_id": group_id,
        }
        group = self.env['account.group'].browse(group_id).exists()
        sign = self.get_balance_sign(group_id=group)
        r_data["balance"] *= sign
        return r_data

    def _get_account_line_data(
        self,
        line,
        digits,
        partners_data=None,
        amounts_data=None
    ):
        """Use data of account_type line to prepare the values to be inserted
        in `account_balance_report_account`

        :param line: ``dict`` The line data
        :param partners_data: ``list`` partner data, used to compute which of
            them belongs to an account
        :param account_sign: ``int`` The account sign, can be 1 or -1, used to
            confirm or change account balance value sign
        :param digits: ``int`` The rounding digits, used in float calc

        :return: ``dict`` The dictionary with data to be set in the
            section report
        """

        if not line.get("type", False):
            partners_data = []
            amounts_data = {}

        r_data = {
            **line,
            'account_id': line['id'],
        }
        account_id = line.get('id')
        account = self.env['account.account'].browse(account_id)

        # The sign was computed only for 'account_type' lines because
        # group line don't partecipate in total_balance computation
        sign = self.get_balance_sign(
            account, account.group_id
        )

        if self.show_partner_details:
            balance = amounts_data[account_id].get('balance') * sign
            curr_data = self._get_foreign_currency_data(line, digits)
            account_partners = self._get_account_partners(
                amounts_data[account_id],
                partners_data
            )
            partners = []
            for partner_id in account_partners:
                partner_balance = amounts_data[account_id][partner_id]['balance']
                partners.append({
                    'id': partner_id,
                    'balance': partner_balance * sign,
                })

        else:
            partners = partners_data
            curr_data = self._get_foreign_currency_data(line, digits)
            balance = line.get('balance') * sign

        r_data.update({
            'balance': balance,
            'partners': partners,
            **curr_data
        })

        return r_data

    def _get_foreign_currency_data(self, data, digits):
        end_curr_bal = data.get('ending_currency_balance', 0.0)
        curr_data = {
            'ending_currency_balance': end_curr_bal,
        }
        if self.foreign_currency:
            init_curr_bal = data.get('initial_currency_balance', 0.0)
            curr_balance = float_round(
                end_curr_bal - init_curr_bal,
                digits
            )
            curr_data.update({
                'currency_balance': curr_balance,
            })
        else:
            curr_data.update({
                'currency_balance': 0.0,
            })
        return curr_data

    def get_section_balance_vals(
        self,
        data={}
    ):
        """Get the command tuple to get section data

        Used to setup command tuple, to insert values into correct balance
        section

        :param data (dict, optional): The data to setup create dictionary,
            to insert data into correct balance section. Defaults to {}.

        :return tuple: The insert command tuple, with data to create
            `account_balance_report_account` record
        """
        return (
            0,
            0,
            {
                "account_id": data.get('account_id', False),
                "currency_id": data.get('currency_id', False),
                "date_from": self.date_from,
                "date_to": self.date_to,
                "group_id": data.get("group_id", False),
                "hide_line": data.get("hide_account", False),
                "balance": data.get("balance", 0.0),
                "ending_balance": data.get("ending_balance", 0.0),
                "currency_balance": data.get("currency_balance", 0.0),
                "currency_ending_balance": data.get("ending_currency_balance", 0.0),
                "level": data.get("level", 0),
                "code": data.get("code", ""),
                "name": data.get("name", ""),
                "complete_code": data.get('complete_code', ""),
                "report_partner_ids": [
                    (
                        0,
                        0,
                        {
                            "currency_id": data.get('currency_id', False),
                            "date_from": self.date_from,
                            "date_to": self.date_to,
                            "report_id": self.id,
                            "balance": p.get('balance', 0.0),
                            "partner_id": p.get('id'),
                        },
                    )
                    for p in data.get('partners', [])
                ],
            },
        )

    def get_total_balance(self, total_debit, total_credit, digits):
        if float_compare(total_credit, total_debit, digits) == 1:
            total_balance = float_round(total_credit - total_debit, digits)
        elif float_compare(total_credit, total_debit, digits) == -1:
            total_balance = float_round(total_debit - total_credit, digits)
        else:
            total_balance = 0.0
        return total_balance

    def get_balance_sign(self, account_id=None, group_id=None):
        sign = 1
        if account_id:
            sign = account_id.user_type_id.account_balance_sign
        elif group_id:
            sign = group_id.account_balance_sign
        return sign

    def _get_account_partners(self, account_data, partners):
        """Get the partner(s) that belong to an account

        :param account_data: ``dict`` The account amounts data, including
            partner id reference
        :param partners: ``dict`` Partners data, contain id and name

        :return: ``list`` partner data to be inserted in
            `account_balnace_report_partner` belonging to and
            `account_balance_report_account`
        """
        account_partners = []
        if isinstance(partners, dict):
            account_partners = [
                p_id for p_id in partners.keys() if p_id in account_data
            ]
        return account_partners

    def _insert_section_values(
        self,
        section,
        l_sec,
        r_sec,
        credit_section,
        debit_section,
        total_debit,
        total_credit,
        section_vals,
        line,
        digits
    ):
        if section == r_sec:
            credit_section.append(section_vals)
            if line.get('type', '') != self.GROUP_TYPE:
                total_credit += line.get('balance')

        elif section == l_sec:
            debit_section.append(section_vals)
            if line.get('type', '') != self.GROUP_TYPE:
                total_debit += line.get('balance')

        return float_round(total_debit, digits), \
            float_round(total_credit, digits)

    def _get_filtered_account(self, accounts_data, section_vals):
        account_data = {}
        for sec_val in section_vals:
            sec_val_account_id = sec_val[2]['account_id']
            if sec_val_account_id in accounts_data.keys():
                account_data[sec_val_account_id] = accounts_data.keys()
        return account_data

    def _get_group_data(self, accounts_data, total_amounts):
        account_obj = self.env['account.account']
        groups_ids = {}
        for account_id in accounts_data.keys():
            account = account_obj.browse(account_id).exists()
            if account.group_id:
                if account.group_id.id not in groups_ids:
                    groups_ids.update({account.group_id.id: [account.id]})
                else:
                    groups_ids[account.group_id.id].append(account.id)

        groups = self.env['account.group'].browse(groups_ids.keys()).exists()
        groups_data = {}
        for group in groups:
            groups_data.update(
                {
                    group.id: {
                        "group_id": group.id,
                        "code": group.code_prefix_start,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "type": "group_type",
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "initial_balance": 0.0,
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": 0.0,
                        "ending_balance": 0.0,
                    }
                }
            )
            if self.foreign_currency:
                groups_data[group.id]["initial_currency_balance"] = 0.0
                groups_data[group.id]["ending_currency_balance"] = 0.0
        group_obj = self.env['account.group']
        for group_id, group_accounts in groups_ids.items():
            for account_id in group_accounts:
                t_a_init_bal = total_amounts[account_id]['initial_balance']
                t_a_debit = total_amounts[account_id]['debit']
                t_a_credit = total_amounts[account_id]['credit']
                t_a_balance = total_amounts[account_id]['balance']
                t_a_end_bal = total_amounts[account_id]['ending_balance']
                groups_data[group_id]['initial_balance'] += t_a_init_bal
                groups_data[group_id]['debit'] += t_a_debit
                groups_data[group_id]['credit'] += t_a_credit
                groups_data[group_id]['balance'] += t_a_balance
                groups_data[group_id]['ending_balance'] += t_a_end_bal
                if self.foreign_currency:
                    t_a_init_curr_bal = total_amounts[account_id]['initial_currency_balance']
                    t_a_end_curr_bal = total_amounts[account_id]['ending_currency_balance']
                    groups_data[group_id]["initial_currency_balance"] += t_a_init_curr_bal
                    groups_data[group_id]["ending_currency_balance"] += t_a_end_curr_bal
            group = group_obj.browse(group_id).exists()
            grp_sign = self.get_balance_sign(group_id=group)
            groups_data[group_id]['balance'] *= grp_sign
        return groups_data

    def _compute_group_hierarchy(self, groups_data):
        groups = self.env['account.group'].browse(groups_data.keys())
        for group in groups:
            parent_id = groups_data[group.id]["parent_id"]
            while parent_id:
                if parent_id not in groups_data.keys():
                    parent_group = self.env["account.group"].browse(parent_id)
                    groups_data[parent_group.id] = {
                        "group_id": parent_group.id,
                        "code": parent_group.code_prefix_start,
                        "name": parent_group.name,
                        "parent_id": parent_group.parent_id.id,
                        "parent_path": parent_group.parent_path,
                        "complete_code": parent_group.complete_code,
                        "account_ids": parent_group.compute_account_ids.ids,
                        "type": "group_type",
                        "initial_balance": 0,
                        "debit": 0,
                        "credit": 0,
                        "balance": 0,
                        "ending_balance": 0,
                    }
                    if self.foreign_currency:
                        groups_data[parent_group.id].update(
                            initial_currency_balance=0,
                            ending_currency_balance=0,
                        )
                acc_keys = ["debit", "credit", "balance"]
                acc_keys += ["initial_balance", "ending_balance"]
                for acc_key in acc_keys:
                    groups_data[parent_id][acc_key] += groups_data[group.id][acc_key]
                if self.foreign_currency:
                    groups_data[group.id]["initial_currency_balance"] += groups_data[
                        group.id
                    ]["initial_currency_balance"]
                    groups_data[group.id]["ending_currency_balance"] += groups_data[
                        group.id
                    ]["ending_currency_balance"]
                parent_id = groups_data[parent_id]["parent_id"]

    def _add_group_to_section_vals(self, section_vals, groups_data):
        for group_data in groups_data.values():
            counter = group_data["complete_code"].count("/")
            group_data['level'] = counter
            sect_vals = self.get_section_balance_vals(group_data)
            sect_vals[2]["complete_code"] = group_data["complete_code"]
            section_vals.append(sect_vals)

        account_obj = self.env['account.account']
        for section_val in section_vals:
            data = section_val[2]
            if data.get("account_id"):
                account = account_obj.browse(data["account_id"]).exists()
                if account.group_id:
                    data["complete_code"] = "/".join(
                        [account.group_id.complete_code, data["code"]]
                    )
                else:
                    data["complete_code"] = data["code"]

        section_vals = sorted(section_vals, key=lambda sv: sv[2]["complete_code"])

        for section_val in section_vals:
            data = section_val[2]
            data["level"] = data["complete_code"].count("/")


class ReportAccountBalanceReportAccount(models.TransientModel):
    _name = "account_balance_report_account"
    _description = "Account Balance Report - Account"
    _inherit = "account_financial_report_abstract"
    _order = "complete_code ASC"

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account"
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Account Currency"
    )

    date_from = fields.Date()
    date_to = fields.Date()

    group_id = fields.Many2one(
        comodel_name="account.group",
        string="Account Group"
    )

    hide_line = fields.Boolean(
        string="Hide line"
    )
    level = fields.Integer(
        index=True,
        default=0,
        string="Hierarchy level"
    )

    balance = fields.Float(digits=(16, 2))
    ending_balance = fields.Float(digits=(16, 2))
    currency_balance = fields.Float(digits=(16, 2))
    currency_ending_balance = fields.Float(digits=(16, 2))

    report_partner_ids = fields.One2many(
        "account_balance_report_partner",
        "report_section_id",
    )
    report_credit_id = fields.Many2one(
        "account_balance_report",
        ondelete="cascade"
    )
    report_debit_id = fields.Many2one(
        "account_balance_report",
        ondelete="cascade"
    )

    code = fields.Char(
        string="Line code"
    )

    name = fields.Char(
        string="Line name"
    )

    complete_code = fields.Char(string="Complete line code")

class ReportAccountBalanceReportPartner(models.TransientModel):
    _name = "account_balance_report_partner"
    _description = "Account Balance Report - Partner"
    _inherit = "account_financial_report_abstract"

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Account Currency"
    )

    date_from = fields.Date()
    date_to = fields.Date()
    hide_line = fields.Boolean(compute="_compute_hide_line")
    report_id = fields.Many2one(
        "account_balance_report",
    )
    report_section_id = fields.Many2one(
        "account_balance_report_account", ondelete="cascade"
    )
    partner_id = fields.Many2one(
        "res.partner", required=True
    )

    balance = fields.Float(digits=(16, 2))

    @api.depends(
        "balance",
        "report_id.hide_account_at_0",
    )
    def _compute_hide_line(self):
        if self.report_id.hide_account_at_0:
            for partner_line in self:
                p_bal = partner_line.balance
                digits = partner_line.currency_id.decimal_places
                partner_line.hide_line = float_is_zero(p_bal, digits)
