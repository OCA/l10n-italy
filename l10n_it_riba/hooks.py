from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """If modules account_accountant is installed, moves the RIBA menu under the accounting menu."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    account_accountant_installed = env['ir.module.module'].search([('name', '=', 'account_accountant'), 
        ('state', '=', 'installed')])
    if account_accountant_installed:
        root_menu = env.ref("account_accountant.menu_accounting")
        if root_menu:
            riba_menu = env.ref("l10n_it_riba.menu_riba")
            riba_menu.parent_id = root_menu.id
            