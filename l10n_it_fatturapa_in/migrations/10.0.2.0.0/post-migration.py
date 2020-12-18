from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        invoices = env['account.invoice'].search([])
        # in order to prevent error messages in old invoices,
        # where ftpa_withholding_amount is 0
        for invoice in invoices:
            invoice.withholding_tax_amount = \
                sum(invoice.ftpa_withholding_ids.mapped('amount'))
