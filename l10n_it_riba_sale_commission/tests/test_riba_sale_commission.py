# Copyright 2023 Nextev
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import Form, TransactionCase


class TestRibaCommission(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.distinta_model = cls.env["riba.slip"]
        cls.commission_model = cls.env["commission"]
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
        cls.partial_commission_net_paid = cls.commission_model.create(
            {
                "name": "20% fixed commission (Net amount) - Payment Based - Partial",
                "fix_qty": 20.0,
                "invoice_state": "paid",
                "amount_base_type": "net_amount",
                "payment_amount_type": "paid",
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
                    "account_type",
                    "=",
                    "income_other",
                ),
                ("company_id", "=", cls.env.company.id),
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
                    "account_type",
                    "=",
                    "expense",
                ),
                ("company_id", "=", cls.env.company.id),
            ],
            limit=1,
        )
        cls.bank_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "asset_cash",
                ),
                ("company_id", "=", cls.env.company.id),
            ],
            limit=1,
        )
        cls.unsolved_account = cls.env["account.account"].create(
            {
                "code": "PastDue",
                "name": "Past Due Bills Account (test)",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )
        cls.account_rec1_id = cls.account_model.create(
            dict(
                code="custacc",
                name="customer account",
                account_type="asset_receivable",
                reconcile=True,
            )
        )
        cls.sbf_effects = cls.env["account.account"].create(
            {
                "code": "STC",
                "name": "STC Bills (test)",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )
        cls.riba_account = cls.env["account.account"].create(
            {
                "code": "RiBa",
                "name": "RiBa Account (test)",
                "account_type": "asset_fixed",
            }
        )
        cls.company_bank = cls.env.ref("l10n_it_riba.company_bank")
        cls.riba_config = cls.env["riba.configuration"].create(
            {
                "name": "Subject To Collection",
                "type": "sbf",
                "bank_id": cls.company_bank.id,
                "acceptance_journal_id": cls.bank_journal.id,
                "credit_journal_id": cls.bank_journal.id,
                "acceptance_account_id": cls.sbf_effects.id,
                "credit_account_id": cls.riba_account.id,
                "bank_account_id": cls.bank_account.id,
                "bank_expense_account_id": cls.expenses_account.id,
                "past_due_journal_id": cls.bank_journal.id,
                "overdue_effects_account_id": cls.unsolved_account.id,
                "protest_charge_account_id": cls.expenses_account.id,
                "settlement_journal_id": cls.bank_journal.id,
            }
        )
        cls.company = cls.env.ref("base.main_company")
        cls.res_partner_model = cls.env["res.partner"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.partner.write({"agent": False})
        cls.sale_order_model = cls.env["sale.order"]
        cls.advance_inv_model = cls.env["sale.advance.payment.inv"]
        cls.settle_model = cls.env["commission.settlement"]
        cls.make_settle_model = cls.env["commission.make.settle"]
        cls.make_inv_model = cls.env["commission.make.invoice"]
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

        cls.payment_term = cls._create_riba_pterm(cls)
        cls.partial_payment_term = cls._create_riba_partials_pterm(cls)
        cls.env["res.partner.bank"].create(
            {
                "acc_number": "IT59R0100003228000000000622",
                "company_id": cls.env.company.id,
                "partner_id": cls.partner.id,
            }
        )

    def _create_invoice(self, inv_date, payment_term, commission, agent=None):
        if agent is None:
            agent = self.agent_monthly
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        return self.env["account.move"].create(
            {
                "invoice_date": inv_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": payment_term.id,
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
                                        "agent_id": agent.id,
                                        "commission_id": commission.id,
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
                            "months": 1,
                            "days": 1,
                        },
                    )
                ],
            }
        )

    def _create_riba_partials_pterm(self):
        return self.env["account.payment.term"].create(
            {
                "name": "C/O 30% Now, Balance 60 Days",
                "riba": True,
                "riba_payment_cost": 0,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "value_amount": 30,
                            "months": 0,
                            "days": 30,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "months": 0,
                            "days": 60,
                        },
                    ),
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
            "settlement_type": "sale_invoice",
        }
        if agent:
            vals["agent_ids"] = [(4, agent.id)]
        wizard = self.make_settle_model.create(vals)
        wizard.action_settle()

    def register_payment(self, invoice, payment_date=None):
        invoice.action_post()

        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config.id}
        )

        riba_move_line_id = False
        for move_line in invoice.line_ids:
            if move_line.account_id.id == self.account_rec1_id.id:
                riba_move_line_id = move_line.id
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        riba_list._compute_acceptance_move_ids()
        wiz_accreditation = (
            self.env["riba.credit"]
            .with_context(
                active_model="riba.slip",
                active_ids=[riba_list_id],
                active_id=riba_list_id,
            )
            .create(
                {
                    "bank_amount": invoice.amount_total - invoice.amount_residual,
                }
            )
        )
        wiz_accreditation.create_move()

        payment_wizard_action = riba_list.settle_all_line()
        payment_wizard_form = Form(
            self.env[payment_wizard_action["res_model"]].with_context(
                **payment_wizard_action["context"]
            )
        )
        if payment_date:
            payment_wizard_form.payment_date = payment_date
        payment_wizard = payment_wizard_form.save()
        payment_wizard.pay()

    def test_riba_settlement(self):
        date = fields.Date.today()
        invoice = self._create_invoice(
            date - relativedelta(days=100), self.payment_term, self.commission_net_paid
        )
        self.register_payment(invoice)
        invoice_not_settle = self._create_invoice(
            date - relativedelta(days=8), self.payment_term, self.commission_net_paid
        )
        self.register_payment(invoice_not_settle)
        self._settle_agent(self.agent_monthly, 1)
        settlements = self.env["commission.settlement"].search(
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

    def test_riba_partial_settlement(self):
        date = fields.Date.today()
        invoice = self._create_invoice(
            date, self.partial_payment_term, self.partial_commission_net_paid
        )
        self.register_payment(invoice)
        self._settle_agent(self.agent_monthly, 1, date_payment_to=datetime.now())
        settlements = self.env["commission.settlement"].search(
            [
                (
                    "agent_id",
                    "=",
                    self.agent_monthly.id,
                ),
                ("state", "=", "settled"),
            ]
        )
        self.assertEqual(0, len(settlements))

    def test_settle_invoice_on_payment_date(self):
        """When commission is "Payment Date Based",
        the commission is settled based on the due date of the RiBa line.
        """
        # Arrange
        commission = self.commission_model.create(
            {
                "name": "20% based on payment date",
                "fix_qty": 20.0,
                "amount_base_type": "net_amount",
                "invoice_state": "paid_date",
            }
        )
        agent = self.agent_monthly
        agent.commission_id = commission
        invoice = self._create_invoice(
            "2020-01-15",
            self.payment_term,
            commission,
            agent=agent,
        )
        self.register_payment(
            invoice,
            payment_date="2020-02-15",
        )

        # Act
        self._settle_agent(agent=agent, date="2020-02-01")
        january_settlement = self.settle_model.search([("state", "=", "settled")])
        self._settle_agent(agent=agent, date="2020-03-01")
        february_settlement = self.settle_model.search([("state", "=", "settled")])

        # Assert
        self.assertFalse(january_settlement)
        self.assertEqual(invoice, february_settlement.line_ids.invoice_line_id.move_id)
