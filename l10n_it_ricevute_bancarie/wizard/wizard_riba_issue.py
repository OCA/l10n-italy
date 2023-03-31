# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, exceptions, fields, models


# -------------------------------------------------------
#        RIBA ISSUE
# -------------------------------------------------------
class RibaIssue(models.TransientModel):
    _name = "riba.issue"
    _description = "Cash Orders Issue"
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
                "distinta_id": rd_id,
                "due_date": date_maturity,
                "partner_id": partner_id,
                "state": "draft",
                "acceptance_account_id": acceptance_account_id,
            }
            return riba_list_line.create(rdl)

        self.ensure_one()
        # Qui creiamo la distinta
        # wizard_obj = self.browse(cr, uid, ids)[0]
        # active_ids = context and context.get('active_ids', [])
        riba_list = self.env["riba.distinta"]
        riba_list_line = self.env["riba.distinta.line"]
        riba_list_move_line = self.env["riba.distinta.move.line"]
        move_line_obj = self.env["account.move.line"]

        # create distinta
        rd = {
            "name": self.env["ir.sequence"].next_by_code("seq.riba.distinta"),
            "config_id": self.configuration_id.id,
            "user_id": self._uid,
            "date_created": fields.Date.context_today(self),
        }
        rd_id = riba_list.create(rd).id

        # group by partner and due date
        grouped_lines = {}
        move_lines = move_line_obj.search([("id", "in", self._context["active_ids"])])
        do_group_riba = True
        if (
            len(
                {
                    "{}{}".format(x.cig, x.cup)
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
                raise exceptions.Warning(
                    _("No bank has been specified for invoice %s")
                    % move_line.move_id.name
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
        mod_obj = self.env["ir.model.data"]
        act_obj = self.env["ir.actions.act_window"]
        action = mod_obj.get_object_reference(
            "l10n_it_ricevute_bancarie", "distinta_riba_action"
        )
        view = mod_obj.get_object_reference(
            "l10n_it_ricevute_bancarie", "view_riba_distinta_form"
        )
        action_id = action and action[1] or False
        action = act_obj.browse(action_id)
        action_vals = action.read()[0]
        action_vals["views"] = [(view and view[1] or False, "form")]
        action_vals["res_id"] = rd_id
        return action_vals
