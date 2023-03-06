from odoo import models, fields, api, exceptions, _
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class SaleCommissionMakeSettle(models.TransientModel):
    _inherit = "sale.commission.make.settle"

    @api.multi
    def action_settle(self):
        self.ensure_one()
        agent_line_obj = self.env['account.invoice.line.agent']
        settlement_obj = self.env['sale.commission.settlement']
        settlement_line_obj = self.env['sale.commission.settlement.line']
        settlement_ids = []
        if not self.agents:
            self.agents = self.env['res.partner'].search(
                [('agent', '=', True)])
        date_to = self.date_to
        for agent in self.agents:
            date_to_agent = self._get_period_start(agent, date_to)
            # Get non settled invoices
            agent_lines = agent_line_obj.search(
                [('invoice_date', '<=', date_to),
                ('invoice_date', '>', date(2022, 1, 1)),
                ('agent', '=', agent.id),
                ('settled', '=', False)], order='invoice_date')
            for line in agent_lines:
                if line.invoice.no_commission:
                    agent_lines = agent_lines - line
                elif line.invoice.payment_term_id.riba:
                    if line.invoice.is_unsolved or line.invoice.date_due + timedelta(days=+5) > date.today():
                        agent_lines = agent_lines - line
            for company in agent_lines.mapped('company_id'):
                agent_lines_company = agent_lines.filtered(
                    lambda r: r.object_id.company_id == company)
                if not agent_lines_company:
                    continue
                pos = 0
                sett_to = date(year=1900, month=1, day=1)
                while pos < len(agent_lines_company):
                    line = agent_lines_company[pos]
                    pos += 1
                    if line._skip_settlement():
                        continue
                    if line.invoice_date > sett_to:
                        # per compatibilità vecchio sistema
                        sett_from = self._get_period_start(
                            agent, line.invoice_date)
                        sett_to = self._get_next_period_date(
                            agent, sett_from,
                        ) - timedelta(days=1)
                        settlement1 = self._get_settlement(
                            agent, company, sett_from, sett_to)
                        # nuovo sistema
                        sett_from = date_to_agent
                        sett_to = self._get_next_period_date(
                            agent, sett_from,
                        ) - timedelta(days=1)
                        settlement2 = self._get_settlement(
                            agent, company, sett_from, sett_to)

                        if not settlement1:
                            if settlement2:
                                settlement=settlement2
                            else:
                                settlement = settlement_obj.create(
                                    self._prepare_settlement_vals(
                                        agent, company, sett_from, sett_to))
                        else:
                            settlement = settlement1
                        settlement_ids.append(settlement.id)
                    settlement_line_obj.create({
                        'settlement': settlement.id,
                        'agent_line': [(6, 0, [line.id])],
                    })
        # go to results
        if len(settlement_ids):
            return {
                'name': _('Created Settlements'),
                'type': 'ir.actions.act_window',
                'views': [[False, 'list'], [False, 'form']],
                'res_model': 'sale.commission.settlement',
                'domain': [['id', 'in', settlement_ids]],
            }

        else:
            return {'type': 'ir.actions.act_window_close'}
