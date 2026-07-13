# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    # =================================================================
    # Concern A - Invoice paid by the travel agency (pure accounting)
    # -----------------------------------------------------------------
    # Ported ~1:1 from the Odoo 16 module. This part only depends on
    # `account` and has nothing to do with e-invoicing.
    # =================================================================
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
        posted = super()._post(soft=soft)
        for invoice in self.filtered(
            lambda move: move.is_invoice(include_receipts=True)
        ):
            if invoice.agent_74ter_id and invoice.to_be_paid_by_agent_74ter:
                invoice._create_74ter_agency_payment_entry()
        return posted

    def _create_74ter_agency_payment_entry(self):
        """Write off the customer receivable in favour of the agency receivable.

        Creates a miscellaneous entry that mirrors the invoice partner lines
        and books the balance on the agency's receivable, then reconciles.
        Ported verbatim from Odoo 16 (the ORM API is unchanged in v18).
        """
        self.ensure_one()
        if not self.company_id.payments_74ter_journal_id:
            raise UserError(
                _('Please set "Journal for agencies payments" in accounting settings')
            )
        credit_amount = 0
        line_names = []
        write_off_vals = []
        to_reconcile = self.env["account.move.line"]
        for line in self.line_ids:
            if line.partner_id and line.amount_residual:
                to_reconcile |= line
                credit_amount += line.amount_residual
                line_names.append(line.name)
                write_off_vals.append(
                    (
                        0,
                        0,
                        {
                            "debit": line.credit,
                            "credit": line.debit,
                            "account_id": line.account_id.id,
                            "partner_id": line.partner_id.id,
                            "name": line.name,
                        },
                    )
                )
        if credit_amount != 0 and write_off_vals:
            agent = self.agent_74ter_id
            write_off_vals.append(
                (
                    0,
                    0,
                    {
                        "debit": abs(credit_amount) if credit_amount > 0 else 0,
                        "credit": abs(credit_amount) if credit_amount < 0 else 0,
                        "account_id": agent.property_account_receivable_id.id,
                        "partner_id": agent.id,
                        "name": ", ".join(line_names),
                    },
                )
            )
            move = self.env["account.move"].create(
                {
                    "journal_id": self.company_id.payments_74ter_journal_id.id,
                    "line_ids": write_off_vals,
                    "move_type": "entry",
                    "date": self.invoice_date,
                    "ref": self.ref,
                }
            )
            move._post()
            to_reconcile |= move.line_ids.filtered(
                lambda ml: ml.partner_id == self.partner_id
            )
            to_reconcile.reconcile()

    # =================================================================
    # Concern B - FatturaPA (art. 74-ter self-billing, RegimeFiscale RF11)
    # -----------------------------------------------------------------
    # Rewritten on top of Odoo 18 CORE `l10n_it_edi`
    # (odoo/addons/l10n_it_edi/models/account_move.py). In v16 this logic
    # lived in the export wizard `wizard.export.fatturapa` and mutated tax
    # records at export time; both are gone in v18.
    #
    # Design decisions taken for this port:
    #   * Trigger: force the CORE self-invoice flag for bills from a 74-ter
    #     agent, so core swaps seller=agency / buyer=company in the XML.
    #   * Natura is driven by the tax configuration in both cases (spec
    #     NTO74-23), consistently with how core reads it from
    #     `account.tax.l10n_it_exempt_reason`:
    #       - extra-EU / non-taxable: a 0% tax carrying nature N3.6 - emitted
    #         as-is (core already renders it, no override needed);
    #       - intra-EU: a 22% reverse-charge tax carrying nature N6.9, kept at
    #         22% for the VAT registers but exported WITHOUT VAT. Any VAT line
    #         with a rate > 0 is therefore forced to AliquotaIVA/Imposta 0 while
    #         its Natura is preserved from the tax (value-builder overrides
    #         below), leaving the accounting untouched. If such a tax carries no
    #         nature, N6.9 is used as a fallback.
    #   * TipoDocumento TD01 and CodiceDestinatario = the agency's SdI code,
    #     as in the Odoo 16 module.
    # =================================================================
    def _l10n_it_edi_is_74ter_self_billing(self):
        """Return True for a 74-ter self-billing autofattura.

        i.e. a purchase document whose supplier (the travel agency) is a
        74-ter agent, issued by a company under the RF11 tax system.
        """
        self.ensure_one()
        # Resolve the EDI company (a branch's root) exactly as core does when
        # it builds the XML values, so the RF11 check matches the rendered
        # RegimeFiscale.
        company = self.company_id._l10n_it_get_edi_company()
        # Receipts are excluded (default include_receipts=False): core never
        # treats a receipt as a self-invoice and does not export it as
        # FatturaPA, so we mirror core's _compute_l10n_it_edi_is_self_invoice.
        return bool(
            self.is_purchase_document()
            and self.commercial_partner_id.is_74ter_agent
            and company.l10n_it_tax_system == "RF11"
        )

    # The parent depends (move_type, line_ids.tax_tag_ids) are NOT inherited
    # automatically when the compute method is overridden, so we repeat them.
    @api.depends(
        "move_type",
        "line_ids.tax_tag_ids",
        "commercial_partner_id.is_74ter_agent",
        "company_id.l10n_it_tax_system",
    )
    def _compute_l10n_it_edi_is_self_invoice(self):
        # Core computes the standard reverse-charge self-invoice flag from the
        # VJ tax-grid tags; we additionally force it for 74-ter bills so that:
        #   * core swaps seller=agency / buyer=company when rendering the XML;
        #   * the core "Send to Tax Agency" button (visible when
        #     l10n_it_edi_is_self_invoice is True) appears on the bill, giving
        #     a send path that bypasses the sale-journal auto-send gate.
        res = super()._compute_l10n_it_edi_is_self_invoice()
        for move in self:
            if move._l10n_it_edi_is_74ter_self_billing():
                move.l10n_it_edi_is_self_invoice = True
        return res

    def _l10n_it_edi_get_values(self, pdf_values=None):
        values = super()._l10n_it_edi_get_values(pdf_values=pdf_values)
        # Always expose `soggetto_emittente` so the QWeb override is safe for
        # every Italian e-invoice (default None -> the template emits TZ).
        values.setdefault("soggetto_emittente", None)
        if self._l10n_it_edi_is_74ter_self_billing():
            # RegimeFiscale RF11 (core forces RF18 for self-invoices).
            values["regime_fiscale"] = "RF11"
            # Ordinary invoice document type, per art. 74-ter guidance.
            values["document_type"] = "TD01"
            # Emitted by the Cessionario/Committente (the tour operator).
            values["soggetto_emittente"] = "CC"
            # ImportoTotaleDocumento must be omitted for this case
            # (the QWeb override drops the element when this is None).
            values["importo_totale_documento"] = None
            # CodiceDestinatario is the agency's SdI code (as in the v16
            # module), not the company's own. <CodiceDestinatario> is rendered
            # from buyer_info['pa_index'], which for a self-invoice is the
            # company; override it with the agency's (the bill partner).
            values["buyer_info"] = {
                **values["buyer_info"],
                "pa_index": self.commercial_partner_id._l10n_it_edi_get_values()[
                    "pa_index"
                ],
            }
        return values

    def _l10n_it_edi_add_base_lines_xml_values(
        self, base_lines_aggregated_values, is_downpayment
    ):
        super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values, is_downpayment
        )
        if not self._l10n_it_edi_is_74ter_self_billing():
            return
        # Intra-EU 74-ter: a line taxed at 22% (kept for the VAT registers) must
        # be exported without VAT, keeping the nature carried by the tax
        # (N6.9), per DettaglioLinee.
        for base_line, _aggregated_values in base_lines_aggregated_values:
            it_values = base_line["it_values"]
            if any(rate > 0 for rate in it_values.get("aliquota_iva_list", [])):
                it_values["aliquota_iva_list"] = [0.0]
                if not it_values.get("natura"):
                    it_values["natura"] = "N6.9"

    def _l10n_it_edi_get_tax_lines_xml_values(
        self, base_lines_aggregated_values, values_per_grouping_key
    ):
        tax_lines = super()._l10n_it_edi_get_tax_lines_xml_values(
            base_lines_aggregated_values, values_per_grouping_key
        )
        if self._l10n_it_edi_is_74ter_self_billing():
            # Same intra-EU rule for the DatiRiepilogo summary block.
            for tax_line in tax_lines:
                if tax_line["aliquota_iva"] and tax_line["aliquota_iva"] > 0:
                    tax_line["aliquota_iva"] = 0.0
                    tax_line["imposta"] = 0.0
                    if not tax_line.get("natura"):
                        tax_line["natura"] = "N6.9"
        return tax_lines
