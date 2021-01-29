from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    invoices = env['account.invoice'].search([
        ('payment_term_id.riba', '=', True), ('riba_partner_bank_id', '=', False)
    ])
    for invoice in invoices:
        invoice._onchange_riba_partner_bank_id()
