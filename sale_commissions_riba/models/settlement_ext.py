from odoo import api, exceptions, fields, models, _


class SettlementExtended(models.Model):
    _inherit = "sale.commission.settlement.line"

    partner = fields.Char(string="Cliente", related="invoice.partner_id.name")
    imponibile = fields.Monetary(string="Imponibile", related="invoice.amount_untaxed")
    tot_invoice = fields.Monetary(string="Totale", related="invoice.amount_total")
    invoice_state = fields.Selection(string="Stato fattura", related="invoice.state")
    payment_date = fields.Date(string="Data pagamento cliente", compute="_get_payment_date")

    @api.depends("invoice.payment_move_line_ids")
    def _get_payment_date(self):
        for line in self:
            date = line.invoice.payment_move_line_ids.sorted("date", reverse = True)
            if date:
                line.payment_date = date[0].date
