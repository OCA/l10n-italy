# -*- coding: utf-8 -*-

# Copyright 2020 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, SUPERUSER_ID


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
            u"Redditi derivanti dall’utilizzazione economica di opere "
            u"dell’ingegno, di brevetti industriali e di processi, formule e "
            u"informazioni relativi a esperienze acquisite in campo "
            u"industriale, commerciale o scientifico, che sono percepiti dagli "
            u"aventi causa a titolo gratuito (ad es. eredi e "
            u"legatari dell’autore e inventore)")
        env.ref('l10n_it_causali_pagamento.l').write({'name': name})
