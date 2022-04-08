#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, installed_version):
    """Disable frontend reprint for existing fiscal printer configurations."""
    pos_configs = env['pos.config'].search([
        ('printer_ip', '!=', False),
        ('iface_reprint_done_order', '=', True),
    ])
    pos_configs.update({
        'iface_reprint_done_order': False,
    })
