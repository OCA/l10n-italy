# Copyright 2023 Nextev
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import SavepointCase


class TestRibaCommission(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.distinta_model = cls.env["riba.distinta"]
        cls.commission_model = cls.env["sale.commission"]
        cls.account_model = cls.env["account.account"]
        cls.move_line_model = cls.env["account.move.line"]

        cls.commission_net_paid = cls.commission_model.create(
            {
                "name": "20% fixed commission (Net amount) - Payment Based",
                "fix_qty": 20.0,
                "invoice_state": "paid",
                "amount_base_type": "net_amount",
            }
        )
        cls.commission_section_paid = cls.commission_model.create(
            {
                "name": "Section commission - Payment Based",
                "commission_type": "section",
                "invoice_state": "paid",
                "section_ids": [
                    (0, 0, {"amount_from": 1.0, "amount_to": 100.0, "percent": 10.0})
                ],
                "amount_base_type": "net_amount",
            }
        )
        cls.sale_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        cls.bank_journal = cls.env["account.journal"].search(
            [("type", "=", "bank")], limit=1
        )
        cls.sale_journal = cls.env["account.journal"].search([("type", "=", "sale")])[0]
        cls.expenses_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_expenses").id,
                )
            ],
            limit=1,
        )
        cls.bank_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_liquidity").id,
                )
            ],
            limit=1,
        )
        cls.account_user_type = cls.env.ref("account.data_account_type_receivable")
        cls.unsolved_account = cls.env["account.account"].create(
            {
                "code": "Past Due",
                "name": "Past Due Bills Account (test)",
                "reconcile": True,
                "user_type_id": cls.account_user_type.id,
            }
        )
        cls.account_rec1_id = cls.account_model.create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=cls.account_user_type.id,
                reconcile=True,
            )
        )
        cls.account_asset_user_type = cls.env.ref(
            "account.data_account_type_fixed_assets"
        )
        cls.sbf_effects = cls.env["account.account"].create(
            {
                "code": "STC",
                "name": "STC Bills (test)",
                "reconcile": True,
                "user_type_id": cls.account_user_type.id,
            }
        )
        cls.riba_account = cls.env["account.account"].create(
            {
                "code": "C/O",
                "name": "C/O Account (test)",
                "user_type_id": cls.account_asset_user_type.id,
            }
        )
        cls.company_bank = cls.env.ref("l10n_it_ricevute_bancarie.company_bank")
        cls.riba_config = cls.env["riba.configuration"].create(
            {
                "name": "Subject To Collection",
                "type": "sbf",
                "safety_days": 5,
                "bank_id": cls.company_bank.id,
                "acceptance_journal_id": cls.bank_journal.id,
                "accreditation_journal_id": cls.bank_journal.id,
                "acceptance_account_id": cls.sbf_effects.id,
                "accreditation_account_id": cls.riba_account.id,
                "bank_account_id": cls.bank_account.id,
                "bank_expense_account_id": cls.expenses_account.id,
                "unsolved_journal_id": cls.bank_journal.id,
                "overdue_effects_account_id": cls.unsolved_account.id,
                "protest_charge_account_id": cls.expenses_account.id,
            }
        )
        cls.company = cls.env.ref("base.main_company")
        cls.res_partner_model = cls.env["res.partner"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.partner.write({"agent": False})
        cls.sale_order_model = cls.env["sale.order"]
        cls.advance_inv_model = cls.env["sale.advance.payment.inv"]
        cls.settle_model = cls.env["sale.commission.settlement"]
        cls.make_settle_model = cls.env["sale.commission.make.settle"]
        cls.make_inv_model = cls.env["sale.commission.make.invoice"]
        cls.product = cls.env.ref("product.product_product_5")
        cls.product.list_price = 5  # for testing specific commission section
        cls.commission_product = cls.env["product.product"].create(
            {"name": "Commission test product", "type": "service"}
        )
        cls.product.write({"invoice_policy": "order"})
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "purchase")], limit=1
        )

        cls.agent_monthly = cls.res_partner_model.create(
            {
                "name": "Test Agent - Monthly Net Paid",
                "agent": True,
                "settlement": "monthly",
                "lang": "en_US",
                "commission_id": cls.commission_net_paid.id,
            }
        )

        cls.income_account = cls.env["account.account"].search(
            [
                ("company_id", "=", cls.company.id),
                ("user_type_id.name", "=", "Income"),
            ],
            limit=1,
        )
        cls.payment_term = cls._create_riba_pterm(cls)
        cls.env["res.partner.bank"].create(
            {
                "acc_number": "IT59R0100003228000000000622",
                "company_id": cls.env.company.id,
                "partner_id": cls.partner.id,
            }
        )

    def _create_invoice(self, inv_date):
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        return self.env["account.move"].create(
            {
                "invoice_date": inv_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.payment_term.id,
                "riba_partner_bank_id": self.partner.bank_ids[0].id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "quantity": 1.0,
                            "price_unit": 100.00,
                            "account_id": self.sale_account.id,
                            "agent_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "agent_id": self.agent_monthly.id,
                                        "commission_id": self.commission_net_paid.id,
                                    },
                                )
                            ],
                        },
                    )
                ],
            }
        )

    def _create_riba_pterm(self):
        return self.env["account.payment.term"].create(
            {
                "name": "C/O 30",
                "riba": True,
                "riba_payment_cost": 0,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "option": "day_following_month",
                            "days": 1,
                        },
                    )
                ],
            }
        )

    def _settle_agent(self, agent=None, period=None, date=None, date_payment_to=None):
        vals = {
            "date_to": (
                fields.Datetime.from_string(fields.Datetime.now())
                + relativedelta(months=period)
            )
            if period
            else date,
            "date_payment_to": date_payment_to,
        }
        if agent:
            vals["agent_ids"] = [(4, agent.id)]
        wizard = self.make_settle_model.create(vals)
        wizard.action_settle()

    def register_payment(self, invoice):
        invoice.action_post()

        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config.id}
        )

        riba_move_line_id = False
        for move_line in invoice.line_ids:
            if move_line.account_id.id == self.account_rec1_id.id:
                riba_move_line_id = move_line.id
        action = wizard_riba_issue.with_context(
            {"active_ids": [riba_move_line_id]}
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        riba_list._compute_acceptance_move_ids()
        wiz_accreditation = (
            self.env["riba.accreditation"]
            .with_context(
                {
                    "active_model": "riba.distinta",
                    "active_ids": [riba_list_id],
                    "active_id": riba_list_id,
                }
            )
            .create(
                {
                    "bank_amount": invoice.amount_total,
                }
            )
        )
        wiz_accreditation.create_move()

    def test_riba_settlement(self):
        date = fields.Date.today()
        invoice = self._create_invoice(date - relativedelta(days=100))
        self.register_payment(invoice)
        invoice_not_settle = self._create_invoice(date - relativedelta(days=4))
        self.register_payment(invoice_not_settle)
        self._settle_agent(self.agent_monthly, 1, date_payment_to=datetime.now())
        settlements = self.env["sale.commission.settlement"].search(
            [
                (
                    "agent_id",
                    "=",
                    self.agent_monthly.id,
                ),
                ("state", "=", "settled"),
            ]
        )
        self.assertEqual(1, len(settlements))
        self.assertEqual(1, len(settlements.line_ids))
