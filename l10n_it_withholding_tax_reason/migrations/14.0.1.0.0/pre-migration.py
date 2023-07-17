from odoo.addons.l10n_it_withholding_tax_reason import hooks


def migrate(cr, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    if not installed_version:
        return
    hooks.rename_old_italian_module(cr)
