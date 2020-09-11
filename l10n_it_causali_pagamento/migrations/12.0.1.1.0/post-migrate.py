# Copyright 2020 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Rename:
        code from Z to ZO
        description corresponding to code L
    """
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env.ref('l10n_it_causali_pagamento.z').write({'code': 'ZO'})
        name = (
            "Redditi derivanti dall’utilizzazione economica di opere "
            "dell’ingegno, di brevetti industriali e di processi, formule e "
            "informazioni relativi a esperienze acquisite in campo "
            "industriale, commerciale o scientifico, che sono percepiti dagli "
            "aventi causa a titolo gratuito (ad es. eredi e "
            "legatari dell’autore e inventore)")
        env.ref('l10n_it_causali_pagamento.l').write({'name': name})
