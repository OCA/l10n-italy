# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from datetime import date, timedelta


class SaleCommissionMakeSettle(models.TransientModel):
    _inherit = "sale.commission.make.settle"

    def _get_agent_lines(self, agent, date_to_agent):
        """
        Exclude outstanding invoices, those with Ri.Ba subject to collection payment
        if at least safety days haven't passed since expiration date and those that
        have manually set the flag 'no_commission' (for example if it has been
        outstanding for years now).
        """
        agent_lines = super()._get_agent_lines(agent, date_to_agent)
        # rimuove righe delle fatture che hanno impostato flag "no_commission"
        agent_lines = agent_lines.filtered(lambda al: not al.invoice.no_commission)
        for line in agent_lines:
            # filtro su Ri.Ba
            if line.invoice.payment_term_id.riba:
                # rimuove le righe se ri.ba è insoluta o nel caso sia sbf non siano
                # passati almeno i giorni di sicurezza da data di scadenza del pagamento
                # per tenersi un margine e verificare che sia stata pagata
                riba_mv_line = self.env['riba.distinta.move.line'].search([
                    ('move_line_id.invoice_id', '=', line.invoice.id)
                ])
                riba_type = riba_mv_line.riba_line_id.type
                if line.commission.invoice_state == 'paid' and (
                        line.invoice.is_unsolved or (
                        (line.invoice.date_due + timedelta(
                            days=riba_mv_line.riba_line_id.config_id.safety_days)
                            > date.today())
                        and riba_type == 'sbf')):
                    agent_lines -= line
        return agent_lines
