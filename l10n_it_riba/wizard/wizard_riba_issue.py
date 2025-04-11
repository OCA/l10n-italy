# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang


# -------------------------------------------------------
#        RIBA ISSUE
# -------------------------------------------------------
class RibaIssue(models.TransientModel):
    _name = "riba.issue"
    _description = "RiBa Issue"
    configuration_id = fields.Many2one(
        "riba.configuration", string="Configuration", required=True
    )

    def create_list(self):
        def create_rdl(
            countme, bank_id, rd_id, date_maturity, partner_id, acceptance_account_id
        ):
            rdl = {
                "sequence": countme,
                "bank_id": bank_id,
                "slip_id": rd_id,
                "due_date": date_maturity,
                "partner_id": partner_id,
                "state": "draft",
                "acceptance_account_id": acceptance_account_id,
            }
            return riba_list_line.create(rdl)

        self.ensure_one()
        # controllo che non siano presenti riba già emesse
        self._check_duplicate_riba_emission()
        # Qui creiamo la distinta
        # wizard_obj = self.browse(cr, uid, ids)[0]
        # active_ids = context and context.get('active_ids', [])
        riba_list = self.env["riba.slip"]
        riba_list_line = self.env["riba.slip.line"]
        riba_list_move_line = self.env["riba.slip.move.line"]
        move_line_obj = self.env["account.move.line"]

        # create distinta
        rd = {
            "name": self.env["ir.sequence"].next_by_code("seq.riba.slip"),
            "config_id": self.configuration_id.id,
            "user_id": self._uid,
            "date_created": fields.Date.context_today(self),
        }
        rd_id = riba_list.create(rd).id

        # group by partner and due date
        grouped_lines = {}
        move_lines = move_line_obj.search([("id", "in", self._context["active_ids"])])
        if any(line.parent_state != "posted" for line in move_lines):
            raise UserError(_("It is possible to issue C/O for posted move only!"))
        do_group_riba = True
        if (
            len(
                {
                    f"{x.cig}{x.cup}"
                    for x in move_lines.mapped("move_id.related_documents")
                }
            )
            > 1
        ):
            do_group_riba = False
        if do_group_riba:
            for move_line in move_lines:
                if move_line.partner_id.group_riba:
                    if not grouped_lines.get(
                        (move_line.partner_id.id, move_line.date_maturity), False
                    ):
                        grouped_lines[
                            (move_line.partner_id.id, move_line.date_maturity)
                        ] = []
                    grouped_lines[
                        (move_line.partner_id.id, move_line.date_maturity)
                    ].append(move_line)

        # create lines
        countme = 1

        for move_line in move_lines:
            if move_line.move_id.riba_partner_bank_id:
                bank_id = move_line.move_id.riba_partner_bank_id
            else:
                raise UserError(
                    _(
                        "No bank has been specified for invoice %(invoice)s",
                        invoice=move_line.move_id.name,
                    )
                )
            if move_line.partner_id.group_riba and do_group_riba:
                for key in grouped_lines:
                    if (
                        key[0] == move_line.partner_id.id
                        and key[1] == move_line.date_maturity
                    ):
                        rdl_id = create_rdl(
                            countme,
                            bank_id.id,
                            rd_id,
                            move_line.date_maturity,
                            move_line.partner_id.id,
                            self.configuration_id.acceptance_account_id.id,
                        ).id
                        # total = 0.0
                        # invoice_date_group = ''
                        for grouped_line in grouped_lines[key]:
                            riba_list_move_line.create(
                                {
                                    "riba_line_id": rdl_id,
                                    "amount": grouped_line.amount_residual,
                                    "move_line_id": grouped_line.id,
                                }
                            )
                        del grouped_lines[key]
                        break
            else:
                rdl_id = create_rdl(
                    countme,
                    bank_id.id,
                    rd_id,
                    move_line.date_maturity,
                    move_line.partner_id.id,
                    self.configuration_id.acceptance_account_id.id,
                ).id
                riba_list_move_line.create(
                    {
                        "riba_line_id": rdl_id,
                        "amount": move_line.amount_residual,
                        "move_line_id": move_line.id,
                    }
                )

            countme += 1

        # ----- show slip form
        action_vals = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_riba.slip_riba_action"
        )
        action_vals["res_id"] = rd_id
        return action_vals

    def _check_duplicate_riba_emission(self):
        # recupero linee dove fare riba
        move_lines = self.env["account.move.line"].search(
            [("id", "in", self._context["active_ids"])]
        )
        # preparo variabili strettamente collegate da cui proviene l'errore
        move_lines_error = self.env["account.move.line"]
        riba_line_error = self.env["riba.slip.line"]
        bank_move_error = self.env["account.move"]
        # ciclo le righe da emettere
        for move in move_lines:
            slip_line_ids = move.mapped("slip_line_ids")
            if slip_line_ids.mapped("riba_line_id"):
                # riporto l'errore per dettaglio distinta riba
                riba_line_error |= slip_line_ids.mapped("riba_line_id")
                if slip_line_ids.mapped("riba_line_id").mapped("acceptance_move_id"):
                    # filtro le righe valide (accreditate)
                    bank_move_lines = (
                        slip_line_ids.mapped("riba_line_id")
                        .mapped("acceptance_move_id")
                        .filtered(lambda line: line.state not in ["cancel"])
                    )
                    if bank_move_lines:
                        # riporto l'errore per annullare il movimento contabile
                        bank_move_error |= bank_move_lines
                move_lines_error |= move
        if move_lines_error or riba_line_error or bank_move_error:
            # errore su collegamenti
            invoice_ids = move_lines_error.mapped("move_id")
            # imposto il messaggio
            currency_simbol = self.env.user.company_id.currency_id.symbol
            invoices_ref = ", ".join(inv.display_name for inv in invoice_ids)
            bank_moves_ref = ", ".join(
                b_line.display_name for b_line in bank_move_error
            )
            riba_lines_ref = ", ".join(
                (
                    str(r_line.sequence)
                    + " "
                    + r_line.invoice_number
                    + " "
                    + formatLang(self.env, r_line.amount)
                    + currency_simbol
                )
                for r_line in riba_line_error
            )
            message = _(
                "Cannot issue a new RiBa on the following invoices: %(invoices)s\n"
                "You need to delete the credit and riba bill detail first.\n"
                "Order of elimination: Journal Entries -> Slips Detail\n"
                "Ref. Journal Entries: %(moves)s\n"
                "Ref. Slips Detail: %(slips)s\n"
                "After deleting, issue a new RiBa!\n"
            ) % {
                "invoices": invoices_ref,
                "moves": bank_moves_ref,
                "slips": riba_lines_ref,
            }

            raise UserError(message)
        return True
